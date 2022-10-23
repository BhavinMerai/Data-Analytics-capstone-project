# +++++++++++++++ AN ATTEMPT AT PLOTTING USING PYTHON PANDAS +++++++++++++++

import pandas as pd
import matplotlib.pyplot as plt

df_tripdata_plot = pd.read_csv(r'E:\bhavin\Python_data-analytics\Case-Study-1\2022_tripdata_cleaned.csv')

#print(df_tripdata_plot.head(3))
#print(df_tripdata_plot.info())

#df_tripdata_plot['member_casual'].value_counts().plot(kind='bar')

#df_tripdata_plot['rideable_type'].value_counts().plot(kind='bar')

#df_tripdata_plot.plot(x='rideable_type',y=['member_casual'],kind='bar', stacked=True, color = ['red', 'green'])

#df_tripdata_plot['membership_count'] = df_tripdata_plot['member_casual'].value_counts()
#df_tripdata_plot['bike_type_count'] = df_tripdata_plot['rideable_type'].value_counts()

#df_tripdata_plot.plot(x='bike_type_count', y='membership_count', kind='bar', stacked=True, color=['red', 'green'])
#df_tripdata_plot['hour_of_day'].hist()
#plt.show()