window.dojoConfig={async:!0},window.dojoConfig.locale="en"
var localeFromBrowser=navigator.languages?navigator.languages[0]:navigator.language||navigator.userLanguage,localeFromStorage=localStorage.getItem("locale")
localeFromStorage?window.dojoConfig.locale=localeFromStorage.toLowerCase():localeFromBrowser&&(window.dojoConfig.locale=localeFromBrowser.toLowerCase()),window.dojoConfig.isRTL=!1
for(var queryParams=window.location.href.slice(window.location.href.indexOf("?")+1).split("&"),i=0;i<queryParams.length;i++){var queryParam=queryParams[i].split("=")
"_rtl"===queryParam[0]&&"true"===queryParam[1]&&(window.dojoConfig.isRTL=!0)}window.dojoConfig.isRTL=window.dojoConfig.isRTL||"ar"===window.dojoConfig.locale.toLowerCase()||"he"===window.dojoConfig.locale.toLowerCase()
var dirNode=document.querySelector("html")
dirNode.setAttribute("dir",window.dojoConfig.isRTL?"rtl":"ltr"),dirNode.className+=" "+window.dojoConfig.locale,dirNode.className+=-1!==window.dojoConfig.locale.indexOf("-")?" "+window.dojoConfig.locale.split("-")[0]:"",window.CKEDITOR_BASEPATH=window.location.pathname.replace("index.html","")+"assets/ckeditor/"
