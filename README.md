# physrisk-crop
Crop vulnerability modelling
This repo aims to provide example, usable code for both customisable basic models, and DSSAT implementations, using appropriate input data from an agricultural portfolio.
These files are a work-in-progress, and more files will be added in due course (reserving the right to amend/remove files as needed). 

Basic Drought Analysis for Crops:
This model first merges crop yield and weather data into singular files before analysis. This program also calculates drought information such as the number of short, medium, and long length droughts (5-8, 9-14, & 15+ days respectively), the total precipitation, and the amount of time spent in drought. This program utilizes estimated growing seasons for each crop to limit the drought calculations to a certain time span, and these can be edited as needed The analysis component then brings together the data processed from the other tools into one analysis-focused program. The data is imported into this file and can be edited as desired by the user to do in depth analysis at the total, state, or county level. Some example graphs and data calculations are provided to guide your own analysis. Test data must be in gridded ISO reference format, otherwise it will mean nothing to the model. If you wish, you can edit the file to use geocodes other than ISO, if that fits your dataset or custom API call.

Further (step-by-step) breakdown:
The model is designed to process and analyze crop yield and drought data for different crop types (Corn, Soybean, and Wheat). It uses Pandas for data manipulation and Matplotlib for data visualization. The script follows a series of steps, including data import, data preprocessing, drought calculations, and graphical analysis. Below is a detailed explanation of each section:
* Data Import:
    * The script begins by importing necessary Python libraries, including Pandas and Matplotlib.
    * It defines a base file path (base_filepath) where the processed data is located.
* Data Import (continued):
    * The script imports several CSV files into Pandas DataFrames. These files include data on crop yields (corn_yield, soybean_yield, wheat_yield) and areas of interest (areas_of_interest), which include the geographical reference related to crop production regions under analysis.
* Data Preprocessing:
    * The ISO 3166-1 alpha-2 codes in the crop yield DataFrames are converted into the proper string format (zero-padded to five digits).
* Area of Interest Processing:
    * Lists (corn_area, soybean_area, wheat_area) are created to represent areas of interest for each specific crop.
* More Data Preprocessing:
    * The ANSI codes in the areas_of_interest DataFrame are converted into the proper string format.
* Main Function:
    * The main function is defined to carry out the core processing tasks.
* Crop Data Processing (create_drought_data):
    * This section defines a function create_drought_data that processes drought data for each crop type (Corn, Soybean, Wheat). The function takes the crop type as an input parameter.
    * It sets up data requirements based on the selected crop type, including choosing the appropriate yield data, areas, years, and date ranges.
    * Drought information is calculated for each region and year, including the number of short, medium, and long droughts, total precipitation, and drought durations.
    * The function returns a DataFrame containing drought-related statistics for the selected crop type.
* Drought Calculation (calculate_droughts):
    * This function calculates drought-related statistics for a given area and year. It counts the number of short, medium, and long-length droughts, tracks drought durations, and computes total precipitation.
    * The function returns a dictionary with drought-related data. Inside the main function, a loop iterates through a list of crop types (Corn, Soybean, Wheat). For each crop type, the corresponding create_drought_data function is called to generate drought data, which is then saved to a CSV file.
* Data Visualization:
    * After processing the data, the script sets up plot settings for Matplotlib to create visualizations.
    * It creates various graphs and plots, including average yield, mean total drought time, and mean total precipitation, for each crop type.
    * Additionally, it generates graphs that compare crop yield and drought statistics among different states or areas for each crop type.


Weather data will have to be pulled in through a custom UI, or via the base hazard model for drought from OS-Climate:

from physrisk.api.v1.hazard_data import HazardResource
from physrisk.data.hazard_data_provider import HazardDataHint, SourcePath
from physrisk.data.inventory import EmbeddedInventory, Inventory
from physrisk.kernel import hazards
from physrisk.kernel.hazards import ChronicDrought


To integrate into the vulnerability module of the OS-Climate API, you need to import the relevant libraries:

from physrisk.kernel.vulnerability_model import VulnerabilityModel
from physrisk.api.v1.common import VulnerabilityCurve, VulnerabilityCurves
from physrisk.api.v1.common import VulnerabilityCurve, VulnerabilityCurves
from physrisk.kernel.assets import Asset, AgricultureAsset
from physrisk.kernel.vulnerability_matrix_provider import VulnMatrixProvider
from physrisk.kernel.vulnerability_model import VulnerabilityModel
from ..kernel.hazards import ChronicDrought
from ..kernel.vulnerability_model import applies_to_events, checked_beta_distrib, get_vulnerability_curves_from_resource



DSSAT - how to use:
DSSAT intgrated vulnerability "power" user files assume you are not using the official DSSAT UI, but running it in command-line instead. DSSAT UI tools can be downloaded upon application to https://get.dssat.net/request/?sft=4 
Example soil, weather, and crop management files are included and can be edited as needed, including for the purpose of uploading custom parameters to DSSAT for selection in the simulation. Note that these files can be written in Python and are for illustration purposes, but DSSAT is a FORTRAN based model. For the Python interface, which enables integration, see https://github.com/XiaogangHe/pyDSSAT/tree/master
Further DSSAT integration with the OS-C UI is very much a work-in-progress so is not available at present. Further guidance on how to input asset-level disclosed data into a DSSAT EXP (crop management and experimental data file) will be provided soon as part of this documentation...
Asset data can still be pulled in by the OS-Climate API, but this would be through a translation function that is required via the infrastructure, to parse asset data into DSSAT-compatible files.
