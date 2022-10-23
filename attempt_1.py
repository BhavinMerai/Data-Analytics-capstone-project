# ++++++++++++ CLEANING AND PERFORMING CALCULATION ON DATASETS USING PANDAS

import os
import glob
#importing the pandas module
import pandas as pd
import numpy as np
from datetime import datetime
#from haversine import haversine, Unit
from math import radians, pi



#loading the file path
file_path = r'E:\bhavin\Python_data-analytics\Case-Study-1'

# ******listing files present in the directory**********
#file_list = os.listdir(file_path)
#print(file_list)

# *********reading/listing only csv files from directory*********
trip_data = glob.glob('*.{}'.format('csv'))
#print(trip_data)

# ********building dataframe to merge all csv files**********
df_tripdata = pd.DataFrame()

# ********using append to merge all data from csv files*********
for file in trip_data:
    df_temp = pd.read_csv(file)
    df_tripdata = df_tripdata.append(df_temp, ignore_index = True)

# *******dropping duplicates from data inplace*********
df_tripdata.drop_duplicates(subset="ride_id",keep=False, inplace=True)

# *******dropping null values from data inplace**********
df_tripdata.dropna(how='any', axis=0, inplace = True)

# ----------calculated distance using latitude and longitude-------
# ************wrong formula*************
#df_tripdata['distance'] = df_tripdata['end_lng'] - df_tripdata['start_lng']/df_tripdata['end_lat'] - df_tripdata['start_lat']
#df_tripdata['distance'] = df_tripdata['distance'] * -1

# ********converting object data types to str for further splitting the columns*********** 
df_tripdata['started_at'] = df_tripdata['started_at'].astype(str)
df_tripdata['ended_at'] = df_tripdata['ended_at'].astype(str)


#df_tripdata['ride_length'] = (df_tripdata['ended_at'] - df_tripdata['started_at'])

# ******* splitting columns *******
df_tripdata[['start_date','start_time']] = df_tripdata['started_at'].str.split(' ', expand=True)
df_tripdata[['end_date','end_time']] = df_tripdata['ended_at'].str.split(' ', expand=True)

# ********* converting splitted columns to datetime format *********
df_tripdata['start_date'] = pd.to_datetime(df_tripdata['start_date'])
df_tripdata['start_time'] = pd.to_datetime(df_tripdata['start_time'])
df_tripdata['end_date'] = pd.to_datetime(df_tripdata['end_date'])
df_tripdata['end_time'] = pd.to_datetime(df_tripdata['end_time'])

# ******** performing calculations **********
df_tripdata['days_used'] = (df_tripdata['end_date'] - df_tripdata['start_date']).dt.days
df_tripdata['time_used_m'] = (df_tripdata['end_time'] - df_tripdata['start_time'])/ pd.Timedelta(minutes=1)

#df_tripdata.drop(['redundant'], axis=1,inplace=True)
#df_tripdata.sort_values(by=['days_used'], ascending = True, inplace = True)
#df_tripdata.sort_values(by=['time_used_m'], ascending = True, inplace = True)

# ********* filtering the data to select values greater than and equal to 0 **********
df_tripdata = df_tripdata.loc[(df_tripdata['days_used']>=0) & (df_tripdata['time_used_m']>=0)]

#df_tripdata['time'] = df_tripdata['time'].total_seconds()
#df_temp1['x','y'] = df_tripdata['start_lat','start_lng']
#df_temp2['a','b'] = df_tripdata['end_lat','end_lng']

# ************ converting latitude and longitude values to radian to use in haversine formula*************
df_tripdata['start_lat_rad']=(df_tripdata['start_lat']*pi)/180
df_tripdata['start_lng_rad']=(df_tripdata['start_lng']*pi)/180
df_tripdata['end_lat_rad']=(df_tripdata['end_lat']*pi)/180
df_tripdata['end_lng_rad']=(df_tripdata['end_lng']*pi)/180

# ********** HAVERSINE FORMULA --> using lat & long values to calculate distance in km ************
def haversine(lat1, lon1, lat2, lon2):
    #lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


df_tripdata['distance_in_km'] = haversine(df_tripdata['start_lat_rad'], df_tripdata['start_lng_rad'], df_tripdata['end_lat_rad'],df_tripdata['end_lng_rad'])
# ********** retrieving weekday name from a date ********
df_tripdata['weekday'] = df_tripdata['start_date'].dt.day_name()
# ********** retrieving hour of day-discrete value from time ********
df_tripdata['hour_of_day'] = df_tripdata['start_time'].dt.hour


# *************** Printing options with row values and column names , also generating summary of analysis from specific columns *************

#summary = df_tripdata[['rideable_type','days_used','time_used_m','distance_in_km','weekday','member_casual']].describe(include = 'all')
#summary = df_tripdata['start_station_name'].value_counts()
#print(summary)
#pd.set_option('display.max_columns', None)
#print(df_tripdata[['start_time','hour_of_day']].head(3))
#df_tripdata.info()
#df_tripdata

#null_rows = df_tripdata.loc[df_tripdata.isna().any(axis=1)]
#print(null_rows)


# ************* Exporting specific column values to csv file ***************
#df_tripdata.to_csv("2022_tripdata_cleaned.csv", columns = ['rideable_type','hour_of_day','days_used','time_used_m','distance_in_km','weekday','member_casual'])