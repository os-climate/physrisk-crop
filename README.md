# physrisk-crop
Crop vulnerability modelling
This repo aims to provide example, usable code for both customisable basic models, and DSSAT implementations, using appropriate input data from an agricultural portfolio.
These files are a work-in-progress, and more files will be added in due course (reserving the right to amend/remove files as needed). 

Basic Drought Analysis for Crops:
This model first merges crop yield and weather data into singular files before analysis. This program also calculates drought information such as the number of short, medium, and long length droughts (5-8, 9-14, & 15+ days respectively), the total precipitation, and the amount of time spent in drought. This program utilizes estimated growing seasons for each crop to limit the drought calculations to a certain time span, and these can be edited as needed The analysis component then brings together the data processed from the other tools into one analysis-focused program. The data is imported into this file and can be edited as desired by the user to do in depth analysis at the total, state, or county level. Some example graphs and data calculations are provided to guide your own analysis. Test data must be in gridded ISO reference format, otherwise it will mean nothing to the model. If you wish, you can edit the file to use geocodes other than ISO, if that fits your dataset or custom API call.


DSSAT - how to use:
DSSAT intgrated vulnerability "power" user files assume you are not using the official DSSAT UI, but running it in command-line instead. DSSAT UI tools can be downloaded upon application to https://get.dssat.net/request/?sft=4 
Example soil, weather, and crop management files are included and can be edited as needed, including for the purpose of uploading custom parameters to DSSAT for selection in the simulation. Note that these files can be written in Python and are for illustration purposes, but DSSAT is a FORTRAN based model. For the Python interface, which enables integration, see https://github.com/XiaogangHe/pyDSSAT/tree/master
Further DSSAT integration with the OS-C UI is very much a work-in-progress so is not available at present. Further guidance on how to input asset-level disclosed data into a DSSAT EXP (crop management and experimental data file) will be provided soon as part of this documentation...
