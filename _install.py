#!/usr/bin/env python
# Copyright (c) 2003-2020 ActiveState Software Inc.

#
# ********************************************************************
#  WARNING: Do not run this script directly. Run the main "./install.sh"
#          which will launch this script properly.
# ********************************************************************

"""
    ./install.sh - ActivePython install script

    Usage:
        ./install.sh [options...]

    General Options:
        -h, --help                print this help and exit
        -v, --verbose             verbose output
        -e  --use-env-shebang     rewrite shebang to use /usr/bin/env (ignored on Windows)
        -I, --install-dir <dir>   specify install directory
        -c, --no-com-registration do not register pywin32 COM objects (Windows only)
        -p, --no-path-additions   do not add directories to PATH (Windows only)

    When called without arguments this script will interactively install
    ActivePython. If the install dir is specified then ActivePython will
    be installed without interaction.
"""

import os
import sys
import getopt
import re
import stat
import logging
import subprocess
if sys.platform.startswith("win"):
    try:
        import winreg
    except ImportError:
        import _winreg as winreg  # python2
    import win32gui
if sys.version_info[0] < 3:
    input = raw_input

import sh2
import activestate

# ---- exceptions


class Error(Exception):
    pass

# ---- global data


gDefaultInstallDir = r"/opt/ActivePython-2.7"

_version_ = (0, 1, 0)
log = logging.getLogger("install")

_DEFAULT_OPENSSLDIRS = (
    "/usr/share/ssl",  # RHEL & Fedora
    "/etc/pki/tls",  # Old RHEL & Fedora
    "/usr/lib/ssl",  # Debian
    "/etc/ssl",  # Gentoo
    "/usr/local/ssl",
    "/System/Library/OpenSSL",  # Mac
)

# ---- internal routines and classes

if sys.platform.startswith("win"):
    def _getSystemDrive():
        try:
            return os.environ["SystemDrive"]
        except KeyError:
            raise Error("'SystemDrive' environment variable is not set")


def _getDefaultInstallDir():
    default = gDefaultInstallDir
    if sys.platform.startswith("win") and\
       default.lower().find("%systemdrive%") != -1:
        default = re.compile("%SystemDrive%", re.I).sub(_getSystemDrive(),
                                                        default)
    return default


def _askYesNo(question, default="yes"):
    """Ask the user the given question and their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes", "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise Error("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        # sys.stdout.write('\n')
        if default is not None and choice == '':
            return default
        elif choice in list(valid.keys()):
            return valid[choice]
        else:
            sys.stdout.write("Please repond with 'yes' or 'no' (or 'y' or 'n').\n")


def _validateInstallDir(installDir):
    if os.path.exists(installDir) and not os.path.isdir(installDir):
        raise Error("cannot install to '%s': exists and is not a directory"
                    % installDir)


# Adapted from pywin32/pywin32_postinstall.py::LoadSystemModule()
def _loadPyWin32Module(modname, dirname):
    # See if this is a debug build.
    import imp
    for suffix_item in imp.get_suffixes():
        if suffix_item[0] == '_d.pyd':
            suffix = '_d'
            break
    else:
        suffix = ""
    basename = "%s%d%d%s.dll" % \
               (modname, sys.version_info[0], sys.version_info[1], suffix)
    path = os.path.join(dirname, basename)
    mod = imp.load_module(modname, None, path,
                          ('.dll', 'rb', imp.C_EXTENSION))


def _registerCOMObject(installDir, module, klass_name, register=1):
    # needs to be run in the installed interpreter so that
    # it gets the paths to the objects correct in the registry
    script = os.path.join(installDir, "Scripts", "registerCOMObj.py")
    if register:
        subprocess.check_call([sys.executable,
                        script,
                        "--register",
                        "--module",
                        module,
                        "--class",
                        klass_name])
    else:
        subprocess.check_call([sys.executable,
                        "Scripts/registerCOMObj.py",
                        "--unregister",
                        "--module",
                        module,
                        "--class",
                        klass_name])

# ---- windows reg and key mgmt


def _winregGetEnvKey(key_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, key_name)
    except WindowsError:
        return ''
    return value


def _winregSetEnvKey(key_name, key_value):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, key_name, 0, winreg.REG_EXPAND_SZ, key_value)
    winreg.CloseKey(key)
    # we don't necessarily have access to win32con here
    hwnd_broadcast = 65535  # win32con.HWND_BROADCAST
    wm_settingchange = 26  # win32con.WM_SETTINGCHANGE = win32con.WM_WININICHANGE
    win32gui.SendMessage(hwnd_broadcast, wm_settingchange, 0, 'Environment')


def _list_dedupe(values):
    uniques = []
    for val in values:
        if val not in uniques:
            uniques.append(val)
    return uniques

# _winregUpdatePath will:
#   - retrieve the current Path from the HKCU.Environment registry key
#   - prepend the new paths to it
#   - remove any empty paths
#   - dedupe/uniq the new path list
#   - put the new Path back in HKCU.Environment


def _winregUpdatePath(new_paths):
    cur_paths = _winregGetEnvKey('Path').split(';')
    paths = new_paths + cur_paths
    while '' in paths:
        paths.remove('')
    _winregSetEnvKey('Path', ';'.join(_list_dedupe(paths)))


def _getPyRootRegKeyName():
    ver = "%d.%d" % (sys.version_info[0], sys.version_info[1])
    return "Software\\Python\\PythonCore\\" + ver


def _getPyRootRegKey():
    # Adapted from pywin32/pywin32_postinstall.py::get_root_key()
    root_key_name = _getPyRootRegKeyName()
    try:
        winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root_key_name, winreg.KEY_CREATE_SUB_KEY)
        return winreg.HKEY_LOCAL_MACHINE
    except OSError, details:
        # Either not exist, or no permissions to create subkey means
        # must be HKCU
        return winreg.HKEY_CURRENT_USER


def _setPyRegKeyVal(key_name, value_name, value):
    # Adapted from pywin32/pywin32_postinstall.py::SetPyKeyVal()
    root_key_name = _getPyRootRegKeyName()
    root_hkey = _getPyRootRegKey()
    root_key = winreg.OpenKey(root_hkey, root_key_name)
    try:
        my_key = winreg.CreateKey(root_key, key_name)
        try:
            winreg.SetValueEx(my_key, value_name, 0, winreg.REG_SZ, value)
        finally:
            my_key.Close()
    finally:
        root_key.Close()
    # print("-> %s\\%s[%s]=%r" % (root_key_name, key_name, value_name, value))


def _get_default_openssldir():
    for default_dir in _DEFAULT_OPENSSLDIRS:
        if os.path.isdir(default_dir):
            cert_pem = os.path.join(default_dir, "cert.pem")
            certs_dir = os.path.join(default_dir, "certs")
            if os.path.isfile(cert_pem) or os.path.isdir(certs_dir):
                return default_dir

    return None


def _get_openssldir():
    # Get the openssldir from the command line
    try:
        output = subprocess.check_output('openssl version -d')
    except (OSError, subprocess.CalledProcessError):
        return _get_default_openssldir()

    return str(output).split('"')[1]


# ---- public module interface


def interactiveInstall(registerCOM=True, pathAdditions=True):
    if os.path.exists("./INSTALLDIR/bin/update_check") and 1 == os.system("./INSTALLDIR/bin/update_check"):
        print("Installer superceded")
        sys.exit(0)

    default = _getDefaultInstallDir()
    sys.stdout.write("""\
Enter directory in which to install ActivePython. Leave blank and
press 'Enter' to use the default [%s].
Install directory: """ % default)
    installDir = input().strip()
    if not installDir:
        installDir = default

    norm = os.path.normpath(os.path.expanduser(installDir))
    if os.path.isdir(norm):
        sys.stdout.write("""
'%s' already exists. Installing over existing
Python installations may have unexpected results. Are you
sure you would like to proceed with the installation?
""" % installDir)
        choice = _askYesNo("Proceed?", default="no")
        if choice == "yes":
            pass
        elif choice == "no":
            print("Aborting install.")
            return
    elif os.path.exists(norm):
        raise Error("'%s' exists and is not a directory" % installDir)

    useEnv = False
    if sys.platform.startswith("win"):
        # if the user hasn't specified -n on the command line, registerCOM
        # defaults to True.  As there isn't a way to specify that registerCOM
        # should be False from the command line, it's safe to assume the user
        # hasn't made a conscious decision here and should be asked.  If, on
        # other hand, registerCOM is False, it means that the user *has*
        # consciously specified -n and we should respect that and not bother
        # asking again
        if registerCOM:
            choice = _askYesNo("Do you want to register the pywin32 COM objects?", default="yes")
            if choice != "yes":
                registerCOM = False
        if pathAdditions:
            choice = _askYesNo("Do you want to add directories to PATH?", default="yes")
            if choice != "yes":
                pathAdditions = False
    else:
        choice = _askYesNo("Do you want to rewrite the shebang lines of scripts to use /usr/bin/env?", default="no")
        if choice == "yes":
            useEnv = True

    print()
    install(installDir, useEnv, registerCOM, pathAdditions)

    # now see if user wants to include Komodo in their install
    if os.path.exists("./INSTALLDIR/bin/komodo_download"):
        os.system("./INSTALLDIR/bin/komodo_download")


def install(installDir=None, useEnv=False, registerCOM=False, pathAdditions=False):
    absInstallDir = os.path.abspath(os.path.normpath(
        os.path.expanduser(installDir)))
    os.chdir(os.path.dirname(__file__) or os.curdir)  # change to unpack dir
    print("Installing ActivePython to '%s'..." % absInstallDir)
    _validateInstallDir(absInstallDir)

    if not os.path.exists(absInstallDir):
        os.makedirs(absInstallDir)

    if sys.platform.startswith("win"):
        preserve = False  # Fails on WinNT, at least, with Permission Denied
    else:
        preserve = True

    sh2.cp(os.path.join("INSTALLDIR", "*"),
           dstdir=absInstallDir, preserve=preserve,
           recursive=True)

    if sys.platform.startswith("win"):
        # space added for templating; allows a backslash as the last character in the replaced text
        win_temp_python_path = r'/tmp/ActiveState------------------------------------------please-run-the-install-script-----------------------------------------\ '.strip()
        if activestate.version_info["pywin32_ver"] is not None:
            # Bootstrap the PyWin32 modules so we can use them for some PyWin32
            # setup.
            print("Removing old PyWin32 registry 'Modules' entries...")
            # Directly from pywin32/pywin32_postinstall.py::install():
            for name in "pythoncom pywintypes".split():
                keyname = "Software\\Python\\PythonCore\\" + sys.winver + "\\Modules\\" + name
                for root in winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER:
                    try:
                        winreg.DeleteKey(root, keyname + "\\Debug")
                    except WindowsError:
                        pass
                    try:
                        winreg.DeleteKey(root, keyname)
                    except WindowsError:
                        pass

            scriptDir = os.path.dirname(__file__) or os.curdir
            pySystemFilesDir = os.path.join(scriptDir, "INSTALLDIR")
            _loadPyWin32Module("pywintypes", pySystemFilesDir)
            _loadPyWin32Module("pythoncom", pySystemFilesDir)

            if registerCOM:
                # Register PyWin32 COM modules.
                # Must keep this in sync with pywin32_postinstall.py.
                print("Registering PyWin32 COM modules...")
                com_modules = [
                    # module_name,                      class_names
                    ("win32com.servers.interp", "Interpreter"),
                    ("win32com.servers.dictionary", "DictionaryPolicy"),
                    ("win32com.axscript.client.pyscript", "PyScript"),
                ]
                import win32api
                import winerror
                for module, class_name in com_modules:
                    try:
                        _registerCOMObject(absInstallDir, module, class_name)
                    except win32api.error, ex:
                        if ex.winerror == winerror.ERROR_ACCESS_DENIED:
                            log.warn("could not register sample PyWin32 COM modules: "
                                     "you do not have permission to install COM objects")
                        else:
                            log.warn("unexpected error registering sample PyWin32 "
                                     "COM modules: %s", ex)

            # Register Pythonwin help file in registry.
            chm = os.path.join(absInstallDir, "Doc",
                               "ActivePython%s%s.chm" % sys.version_info[:2])
            try:
                _setPyRegKeyVal("Help\\Pythonwin Reference", None, chm)
            except winreg.error, ex:
                log.info("could not set PythonWin help reference registry key "
                         "(this is not serious): %s", ex)

            # Create win32com\gen_py directory.
            genPy = os.path.join(absInstallDir, "Lib", "site-packages",
                                 "win32com", "gen_py")
            if not os.path.exists(genPy):
                print("Creating '%s'..." % genPy)
                os.makedirs(genPy)

        # TODO:
        # - Warn if there are potentially conflicting py*.dll's in
        #   the system directory and/or just implement copying those over.
        # - Handle any Windows integration. Add options for this.
        #   - program group and shortcuts
        #   - PATH and PATHEXT mods
        #   - file associations

        relocate_manifest_file = os.path.join(absInstallDir, "Lib", "reloc.txt")
        if os.path.exists(relocate_manifest_file):
            print("Updating paths for scripts")
            with open(relocate_manifest_file) as relocate_manifest:
                for relocate_relative_file in relocate_manifest:
                    activestate.relocate_path(
                        os.path.join(absInstallDir, relocate_relative_file.strip()),
                        os.path.join(win_temp_python_path, ''),
                        os.path.join(absInstallDir, ''),
                        log.isEnabledFor(logging.DEBUG))

        dlls_dir = os.path.join(absInstallDir, "DLLs")
        scripts_dir = os.path.join(absInstallDir, "Scripts")
        tools_dir = os.path.join(absInstallDir, "Tools")
        ninja_dir = os.path.join(tools_dir, "ninja")

        # update PATH for current user
        if pathAdditions:
            _winregUpdatePath([absInstallDir, dlls_dir, scripts_dir, tools_dir, ninja_dir])

        new_path = "%s;%s;%s;%s;%s;%%Path%%" % (absInstallDir, dlls_dir, scripts_dir, tools_dir, ninja_dir)
        doc = os.path.join(absInstallDir, "Doc",
                           "ActivePython%s%s.chm" % sys.version_info[:2])
        print("""
ActivePython has been successfully installed to:

    %s

You can add the following to your Path to ensure
ActivePython is available in your environment:

    Path=%s

The documentation is available here:

    %s
    web: http://docs.activestate.com/activepython/

Please send us any feedback you might have or log bugs here:

    activepython-feedback@ActiveState.com
    http://bugs.activestate.com/ActivePython/

Thank you for using ActivePython.""" % (absInstallDir, new_path, doc))

    else:
        print("Relocating dir-dependent files...")
        activestate.relocate_python(install_prefix=absInstallDir,
                                    verbose=log.isEnabledFor(logging.DEBUG),
                                    useEnv=useEnv)

        docDir = os.path.join(absInstallDir, "doc",
                              "python%s.%s" % sys.version_info[:2],
                              "index.html")
        webdoc = 'http://docs.activestate.com/activepython/%s.%s' % \
            sys.version_info[:2]

        opensslDir = _get_openssldir()
        print("""
ActivePython has been successfully installed to:

    %s

You can add the following to your .bashrc (or equivalent)
to put ActivePython on your PATH:

    export PATH=%s/bin:%s/Tools:%s/Tools/ninja:$PATH

If you are running a linux distribution other than CentOS
please set the OPENSSLDIR environment variable to your
system's default OpenSSL certificate directory.
This is our expected value for your system:

    export OPENSSLDIR=%s

The documentation is available here:

    %s
    web: %s

Please send us any feedback you might have or log bugs here:

    activepython-feedback@ActiveState.com
    http://bugs.activestate.com/ActivePython/

Thank you for using ActivePython.
""" % (absInstallDir, absInstallDir, absInstallDir, absInstallDir, opensslDir, docDir, webdoc))


# ---- mainline

def main(argv):
    logging.basicConfig()

    # Parse options.
    try:
        opts, args = getopt.getopt(argv[1:], "VvheI:n", [
            "version", "verbose", "help", "use-env-shebang", "install-dir=", "no-com-registration", "no-path-additions"
        ])
    except getopt.GetoptError, ex:
        log.error(str(ex))
        log.error("Try `./install.sh --help'.")
        return 1
    installDir = None
    registerCOM = True
    pathAdditions = True
    useEnv = False
    for opt, optarg in opts:
        if opt in ("-h", "--help"):
            sys.stdout.write(__doc__)
            return
        elif opt in ("-V", "--version"):
            ver = '.'.join([str(part) for part in _version_])
            print("install %s" % ver)
            return
        elif opt in ("-e", "--use-env-shebang"):
            useEnv = True
        elif opt in ("-v", "--verbose"):
            log.setLevel(logging.DEBUG)
        elif opt in ("-I", "--install-dir"):
            installDir = optarg
        elif opt in ("-c", "--no-com-registration"):
            registerCOM = False
        elif opt in ("-p", "--no-path-additions"):
            pathAdditions = False

    try:
        if installDir is None:
            interactiveInstall(registerCOM, pathAdditions)
        else:
            install(installDir, useEnv, registerCOM, pathAdditions)
    except (EnvironmentError, Error), ex:
        log.error(str(ex))
        # XXX help blurb???
        if log.isEnabledFor(logging.DEBUG):
            print()
            import traceback
            traceback.print_exception(*sys.exc_info())
        return 1
    except KeyboardInterrupt:
        log.debug("user abort")
        pass


if __name__ == "__main__":
    __file__ == sys.argv[0]
    sys.exit(main(sys.argv))
