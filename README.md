# GRFINhelper
The GRFIN yaml generator is a simple python program which creates a yaml file for the USGS GRFIN software to read for inundation modelling using a DEM
Find the latest verison of GRFIN here: https://code.usgs.gov/grfintools/grfintools  
(Note, TauDEM must also be installed, as specified in the GRFIN installation process). https://hydrology.usu.edu/taudem/taudem5/downloads.html  

To use the GRFIN helper, please ensure you have the latest version of Python installed. This can be found here: https://www.python.org/downloads/  

With python installed, right click the "create_grifin_yaml.py" file and select "edit with IDLE" It may say (Run with ArcGIS), this is fine.  

In the IDLE editor, select 'Run' and 'Run Module'. This will begin a dialogue where you may enter important values to the yaml. This will determine what GRFIN does with your DEM.  

Assistance understanding what these options are can be found in the GRFIN documentation on pages 38-55, here: https://pubs.usgs.gov/tm/14/a3/tm14a3.pdf  

Finally, once your yaml file is generated, run it in GRFIN using the command 'grfintools fileName.yaml' in the command prompt. Your outputs will be in the specified location.  
(Note, you need to make sure your directory in command prompt is the same as where your yaml file is located. An example of this is 'cd Documents/fileName.yaml')
