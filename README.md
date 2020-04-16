# covid19viz
New visualization and prediction of COVID-19 in USA, such as Michigan, CA.

    I. Visualize the data of COVID-19 today

    II. View the history data of COVID-19

    III. Predict the future of COVID-19

# Steps
1. Grab data from goverment websites
2. Save to excel file for store
3. Show data in new diagram

# How to run in Windows
1. Download and install python at https://www.python.org/downloads/ to c:/python27
2. Add path c:/python27 to system path of Windows
3. To install pip, download get-pip.py by following this link: https://bootstrap.pypa.io/get-pip.py. Save to c:/python27
4. Go to c:/python27, run python get-pip.py
5. Add path c:/python27/scripts to system path of Windows
6. Run cmd.exe to enter command window, install libraries by 

     pip install opencv-python
     
     pip install pandas
     
     pip install matplotlib
     
     pip install lxml
     
     pip install scipy

7. Run python virusviz18.py
8. Optionally install base map
 
     download and install
     
          http://download.osgeo.org/osgeo4w/osgeo4w-setup-x86_64.exe
   
          https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi
     
     pip install pyproj==1.9.6
   
     set the system environment variable: 
     
                                        GEOS_DIR=C:\OSGeo4W64
   
                                        PROJ_DIR=C:\OSGeo4W64
                                                         
     add    C:\OSGeo4W64\bin to PATH
   
     pip install --user git+https://github.com/matplotlib/basemap.git

# How to run in Ubuntu
1. Run python virusviz18.py

# SIR model
1. Predict with SIR model, referring to Wuhan data


