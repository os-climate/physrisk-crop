import pandas as pd  
import matplotlib.pyplot as plt

base_filepath = '~/Processed_Data/'

# Import data into pandas DataFrames
corn_yield = pd.read_csv(base_filepath+'Cleaned_Corn_Yield.csv')
soybean_yield = pd.read_csv(base_filepath+'Cleaned_Soybean_Yield.csv')
wheat_yield = pd.read_csv(base_filepath+'Cleaned_Wheat_Yield.csv')
areas_of_interest = pd.read_csv(base_filepath+'Areas_of_Interest.csv')

# Turn the ISO 3166-1 alpha-2 codes for yield DataFrames into the proper string format
corn_yield['ISO 3166-1 Code'] = corn_yield['ISO 3166-1 Code'].astype(str).str.zfill(5)
soybean_yield['ISO 3166-1 Code'] = soybean_yield['ISO 3166-1 Code'].astype(str).str.zfill(5)
wheat_yield['ISO 3166-1 Code'] = wheat_yield['ISO 3166-1 Code'].astype(str).str.zfill(5)

# Find the area of interest for each specific crop
corn_area = [str(i).zfill(5) for i in corn_yield['ISO 3166-1 Code'].unique().tolist()]
soybean_area = [str(i).zfill(5) for i in soybean_yield['ISO 3166-1 Code'].unique().tolist()]
wheat_area = [str(i).zfill(5) for i in wheat_yield['ISO 3166-1 Code'].unique().tolist()]

# Turn all ANSI codes in areas_of_interest into the proper string format
areas_of_interest['ISO 3166-1 Code'] = areas_of_interest['ISO 3166-1 Code'].astype(str).str.zfill(5)
# Turns the ANSI codes into the indices of areas_of_interest
areas_of_interest.set_index('ISO 3166-1 Code', inplace=True)

def main():
	# Use the create_drought_data() method to process and create data for each crop
				crop_list = ['Corn', 'Soybean', 'Wheat']
				for crop in crop_list: 
					crop_complete = create_drought_data(crop)
					crop_complete.to_csv(r''+base_filepath+'Final_Data/'+crop+'_Droughts.csv', index=False, header=True)

#--------------------------------------------------------------------------------
# Method definition to create and return the DataFrame with drought information.
#--------------------------------------------------------------------------------
def create_drought_data(crop_type):
	# Sets up loop and data file requirements depending on the type of crop
	if (crop_type == 'Corn'):
		yield_df = corn_yield
		areas = corn_area
		years = range(1991, 2023+1)
		dates = ['-04-01', '-10-31']
	elif (crop_type == 'Soybean'):
		yield_df = soybean_yield
		areas = soybean_area
		years = range(1991, 2022+1)
		dates = ['-05-01', '-11-30']
	elif (crop_type == 'Wheat'):
		yield_df = wheat_yield
		areas = wheat_area
		years = range(1991, 2020+1)
		dates = ['-11-01', '-07-31']
		return create_wheat_drought_data(yield_df=yield_df, area=area, years=list(years), dates=dates)
	else:
		raise Exception("Improper crop type submitted. Please pass 'corn', 'soybean', or 'wheat'.")

	# Create new dataframes to store drought information for each crop using custom drought durations
	droughts = pd.DataFrame(columns=['Year', 'area', 'state', 'Location', #'Yield Value',
									 'Num_Short', 'Periods_S', 'Lengths_S',
									 'Num_Med', 'Periods_M', 'Lengths_M',
									 'Num_Long', 'Periods_L', 'Lengths_L',
									 'Total Precipitation',
									 'Short_Time', 'Med_Time', 'Long_Time',
									 'Total Drought Time', 'Total Drought Percentage'])

	# Create a new row in the DataFrame for each region/year combination
	print(f'\nDrought calculations for {crop_type}:')
	for area in areas:
		print("Calculating drought data for "+areas_of_interest.loc[area, 'Location'])
		state = areas_of_interest.loc[area, 'State Initial']

		# Reads in the weather data set and sets the date column as the index
		weather = pd.read_csv(base_filepath+'Weather_Data/'+state+'_AVGPrecip.csv')
		weather['Date'] = pd.to_datetime(weather['Date'])
		weather.set_index('Date', inplace=True)

		# For each year of interest
		for year in years:
			# Establish the growing season that crosses years
			growth_season = pd.date_range(start=str(year)+dates[0], end=str(year)+dates[1])

			# Calculate the drought data for this county in this year and append it to the DataFrame
			data = calculate_droughts(yield_df=yield_df, area=area, state=state, year=year, 
									  growth_season=growth_season, weather_df=weather)
			droughts = droughts.append(data, ignore_index=True)

		# End of drought data for a single county, loop is repeated for more counties

	yield_df = yield_df[['Year', 'ISO 3166-1 Code', 'Value']].rename(columns={'ISO 3166-1 Code':'County', 'Value':'Yield Value'})
	return droughts.merge(right=yield_df, how='left', on=['Year', 'ISO 3166-1'])

def create_wheat_drought_data(yield_df, area, years, dates, crop_type='wheat'):
	# Create new dataframes to store drought information for each crop using custom drought durations
	droughts = pd.DataFrame(columns=['Year', 'area', 'state', 'Location',
									 'Num_Short', 'Periods_S', 'Lengths_S',
									 'Num_Med', 'Periods_M', 'Lengths_M',
									 'Num_Long', 'Periods_L', 'Lengths_L',
									 'Total Precipitation',
									 'Short_Time', 'Med_Time', 'Long_Time',
									 'Total Drought Time', 'Total Drought Percentage'])
	start_year = years.pop(0)

	print(f'\nDrought calculations for {crop_type}:')
	for area in area:
		print("Calculating drought data for "+areas_of_interest.loc[area, 'Location'])
		state = areas_of_interest.loc[area, 'Region Initial']

		# Reads in the weather data set and sets the date column as the index
		weather = pd.read_csv(base_filepath+'Weather_Data/'+state+'_AVGPrecip.csv')
		weather['Date'] = pd.to_datetime(weather['Date'])
		weather.set_index('Date', inplace=True)

		# For each year of interest
		for year in years:
			# Establish the growing season that crosses years
			growth_season = pd.date_range(start=str(year-1)+dates[0], end=str(year)+dates[1])

			# Calculate the drought data for this area in this year and append it to the DataFrame
			data = calculate_droughts(yield_df=yield_df, area=area, year=year,
									  growth_season=growth_season, weather_df=weather)
			droughts = droughts.append(data, ignore_index=True)

		# End of drought data for a single region, loop is repeated for more areas

	yield_df = yield_df[['Year', 'ISO 3166-1 Code', 'Value']].rename(columns={'ISO 3166-1 Code':'Area', 'Value':'Yield Value'})
	return droughts.merge(right=yield_df, how='left', on=['Year', 'Area'])

def calculate_droughts(yield_df, area, year, growth_season, weather_df):
	# Count the number of short, medium, and long length droughts
		cur_len = 0
		s_date, e_date = '', ''
		total_s, total_m, total_l = 0, 0, 0
		num_days = 0
		total_pcpn = 0

		# Create variable counters to later store in the data dictionary
		num_short, periods_s, lengths_s = 0, '', ''
		num_med, periods_m, lengths_m = 0, '', ''
		num_long, periods_l, lengths_l = 0, '', ''
		
		# Loop through each day in the year calculating drought/weather information
		for day in growth_season:
			num_days += 1  # Increment the number of days
			total_pcpn += weather_df.loc[day, area]  # Add the day's average precipitation

			if (weather_df.loc[day, area] <= 0.00005):  # None to negligible rain -> increase drought length counter
				if cur_len == 0:
					s_date = day  # Start a new drought if necessary
				cur_len += 1

			# Rain has occured and a drought has ended, so end the drought & record drought data to the DataFrame
			elif (weather_df.loc[day, area] > 0.00005 and cur_len >= 5):
				e_date = day  # End date is the first day of rain after drought

				if (cur_len in range(5,9)):  # Short Drought
					num_short += 1
					total_s += cur_len
					if (periods_s!='' and lengths_s!=''):
						periods_s += ', '+str(s_date.date())+' to '+str(e_date.date())
						lengths_s += ', '+str(cur_len)
					else:
						periods_s = str(s_date.date())+' to '+str(e_date.date())
						lengths_s = str(cur_len)

				elif (cur_len in range(9,15)):  # Medium Drought
					num_med += 1
					total_m += cur_len
					if (periods_s!='' and lengths_s!=''):
						periods_s += ', '+str(s_date.date())+' to '+str(e_date.date())
						lengths_s += ', '+str(cur_len)
					else:
						periods_m = str(s_date.date())+' to '+str(e_date.date())
						lengths_m = str(cur_len)

				elif (cur_len >= 15):  # Long Drought
					num_long += 1
					total_l += cur_len
					if (periods_l!='' and lengths_l!=''):
						periods_l += ', '+str(s_date.date())+' to '+str(e_date.date())
						lengths_l += ', '+str(cur_len)
					else:
						periods_l = str(s_date.date())+' to '+str(e_date.date())
						lengths_l = str(cur_len)

				cur_len = 0  # Reset drought duration now that it has ended
				s_date, e_date = '', ''  # Reset drought dates

			else:  # Area got precipitation but no drought was ended: reset the counter
				cur_len = 0 
				s_date, e_date = '', ''  # Reset drought dates
		# Update the data dictionary with the correct information then return it
		total_drought = total_s + total_m + total_l
		# Compute the location for the specific area
		area_location = areas_of_interest.loc[area, 'Location']
		data = {
				'Year': year,
				'Area': area,
				'State': state,
				'Location': area_location,  # Include the computed location here
				'Num_Short': num_short,
				'Periods_S': periods_s,
				'Lengths_S': lengths_s,
				'Num_Med': num_med,
				'Periods_M': periods_m,
				'Lengths_M': lengths_m,
				'Num_Long': num_long,
				'Periods_L': periods_l,
				'Lengths_L': lengths_l,
				'Total Precipitation': total_pcpn,
				'Short_Time': total_s,
				'Med_Time': total_m,
				'Long_Time': total_l,
				'Total Drought Time': total_drought,
				'Total Drought Percentage': total_drought / num_days
				} 
		return data

main()
print('Data has been processed and drought data has been calculated.')

# Import data sets as DataFrames from CSV files
areas_of_interest = pd.read_csv(base_filepath+'Areas_of_Interest.csv')
corn_data = pd.read_csv(base_filepath+'Final_Data/Corn_Droughts.csv')
soybean_data = pd.read_csv(base_filepath+'Final_Data/Soybean_Droughts.csv')
wheat_data = pd.read_csv(base_filepath+'Final_Data/Wheat_Droughts.csv')


# List containing all of the crop files read in and the crop name
crop_DFs = [[corn_data, 'Corn'], [soybean_data, 'Soybean'], [wheat_data, 'Wheat']]  


# Set up plot settings
plt.style.use('seaborn')
plt.rc('font', size=20)          # controls default text sizes
plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=20)    # legend fontsize
plt.rc('figure', titlesize=20, figsize=(15, 8))  # fontsize of the figure title


#--------------------------------------------------------------------
# TEMPORARY REASSIGNMENT!!!!
#crop_DFs = [[wheat_data, 'Wheat']]
#--------------------------------------------------------------------
# Create descriptive statistics for each crop DataFrame
for df in crop_DFs:
	print('\nDescriptive statistics for all states for the number \nof short, medium, and long droughts ('+df[1]+' seasons):')
	columns = ['Num_Short', 'Num_Med', 'Num_Long']
	print(df[0][columns].describe().to_string())

	print('\nDescriptive statistics for all states for the time spent \nin short, medium, and long length droughts ('+df[1]+' seasons):')
	columns = ['Short_Time', 'Med_Time', 'Long_Time']
	print(df[0][columns].describe().to_string())

	print('\nDescriptive statistics for the state average of fraction of time spent in drought per '+df[1]+' season by state:')
	print(df[0].groupby('area')['Total Drought Percentage'].describe().to_string())


# Create and display a graph with the entire mean yield and entire mean time in drought
for df in crop_DFs:
	by_year = df[0].groupby(['Year'])
	ax = plt.subplot(3, 1, 1)
	plt.plot(by_year['Yield Value'].mean(), label='Average Yield', color='green')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Yield (bu/A)')
	plt.title('Average Yield, Average Total Drought Time, & Mean Total Precipitation for '+df[1])

	plt.subplot(3, 1, 2, sharex=ax)
	plt.plot(by_year['Total Drought Time'].mean(), label='Mean Time in Drought', color='red')
	#plt.plot(by_year['Total Short Time'].mean(), label='Mean Time in Short Droughts')
	#plt.plot(by_year['Total Med Time'].mean(), label='Mean Time in Medium Droughts')
	#plt.plot(by_year['Total Long Time'].mean(), label='Mean in Long Droughts')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Days in Drought')

	plt.subplot(3, 1, 3, sharex=ax)
	plt.plot(by_year['Total Precipitation'].mean(), label='Total Precipitation', color='blue')
	plt.legend(bbox_to_anchor=(1,1), loc="upper left")
	plt.ylabel('Precipitation (in.)')

	plt.tight_layout()
	plt.show()


# Create and display graphs for each state and each crop comparing average 
# crop yield and average total drought length
for df in crop_DFs:
	crop_DF = df[0].merge(areas_of_interest[['area', 'State Initial']], 
						  left_on='area', right_on='State Initial')
	for state in crop_DF['State_y'].unique():
		cur_state = crop_DF[crop_DF['State_y']==state]
		by_year = cur_state.groupby(['Year'])

		ax = plt.subplot(3, 1, 1)
		plt.plot(by_year['Yield Value'].mean(), label='Average Yield', color='green')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Yield (bu/A)')
		plt.title('Average '+df[1]+' Yield, Mean Total Drought Time, and Mean Total Precipitation in '+state)

		plt.subplot(3, 1, 2, sharex=ax)
		plt.plot(by_year['Total Drought Time'].mean(), label='Mean Drought Time', color='red')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Days in Drought')

		plt.subplot(3, 1, 3, sharex=ax)
		plt.plot(by_year['Total Precipitation'].mean(), label='Mean Total Precipitation', color='blue')
		plt.legend(bbox_to_anchor=(1,1), loc="upper left")
		plt.ylabel('Precipitation (in.)')

		plt.tight_layout()
		plt.show()

print('Data has been analyzed and plotted.')


