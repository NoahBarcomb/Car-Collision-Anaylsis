from matplotlib import pyplot as plt #graphing
import matplotlib.colors as mcolors #colors
import seaborn as sns #for second question
import pandas #dataframes, easy manipulation
import random #for random color generation
import numpy #numpy module



dataframe = pandas.read_csv("data.csv", dtype = {"Local Case Number": "string"}) #data is imported and Local Case Number is made a string to prevent mixed data types

print(f"[!] Before any data cleaning, there are {len(dataframe.index)} rows in the dataframe.")
#data cleaning

#drop duplicates by looking at the case number
dataframe = dataframe.drop_duplicates("Local Case Number")

print(f"[!] After dropping duplicates based on the Local Case Number column, there are {len(dataframe.index)} rows.")

#drop unwanted columns
unwanted_columns = ['Report Number', 'Agency Name', 'Drivers License State', 'Local Case Number', 'ACRS Report Type', 'Vehicle ID', 'Crash Date/Time', 'Driverless Vehicle', 'Speed Limit', 'Vehicle Going Dir', 'Route Type', 'Road Name', 'Cross-Street Name', 'Off-Road Description', 'Municipality', 'Related Non-Motorist', 'Person ID',
                                'Vehicle First Impact Location', 'Parked Vehicle', 'Latitude', 'Longitude', 'Location', 'Vehicle Body Type', 'Vehicle Year']

dataframe = dataframe.drop(unwanted_columns, axis = 1)

print(f"[!] {len(unwanted_columns)} unwanted columns have been removed.")

#drop any null/NaN/blank values
dataframe = dataframe.dropna(how = 'any', axis = 0)
#drop any rows where the Driver at Fault column has a value of "Unknown"
dataframe = dataframe[dataframe['Driver At Fault'] != "Unknown"]
#drop any rows where the Non-Motorist Substance Abuse column has a value of "UNKNOWN"
dataframe = dataframe[dataframe['Non-Motorist Substance Abuse'] != "UNKNOWN"]


print(f"[!] After dropping rows that contain ANY null value (N/A, null, None, NaN, 0, unknown), there are {len(dataframe.index)} rows.")

#make everything lowercase since nothing needs to be case sensitive
for column in dataframe.columns:
    dataframe[column] = dataframe[column].str.lower()

#drop any rows where the Vehicle Damage Extent column has a value of "other", "unknown"
dataframe = dataframe[dataframe['Vehicle Damage Extent'] != "other"]
#drop any rows where the Vehicle Damage Extent column has a value of "UNKNOWN"
dataframe = dataframe[dataframe['Vehicle Damage Extent'] != "unknown"]


#combine column Vehicle Make & Vehicle Model to make column Vehicle
dataframe['Vehicle'] = dataframe['Vehicle Make'] + " " + dataframe['Vehicle Model']


#First Question Begins Here

#this will show how many types of injuries and types of vehicle damages each car model has had
damage_counts = dataframe.groupby(['Vehicle', 'Vehicle Damage Extent']).size().unstack(fill_value = 0)

filtered = damage_counts.nlargest(10, columns = "no damage")

#x = numpy.arange(10)
width = 10

fig, ax = plt.subplots()
print(filtered)
ax.bar(filtered.index, filtered['destroyed'], label='Destroyed')
ax.bar(filtered.index, filtered['disabling'], bottom=filtered['destroyed'], label='Disabling')
ax.bar(filtered.index, filtered['functional'], bottom=filtered['destroyed'] + filtered['disabling'], label='Functional')
ax.bar(filtered.index, filtered['no damage'], bottom=filtered['destroyed'] + filtered['disabling'] + filtered['functional'], label='No Damage')

ax.set_title("Vehicle Damage Extent Per Car")
ax.set_xlabel("Vehicle Model")
plt.xticks(rotation = 45, ha = 'right')
ax.set_ylabel("Total of all types of wrecks")
ax.legend()
plt.show()

#Second Question Begins Here
injury_counts = dataframe.groupby(['Vehicle', 'Injury Severity']).size().unstack(fill_value = 0)

filtered = injury_counts.nlargest(10, columns = "no apparent injury")

values = filtered.loc[:, 'no apparent injury']

colors = [random.choice(list(mcolors.CSS4_COLORS.values())) for _ in range(10)]


plt.xticks(rotation = 45, ha = 'right')
plt.title("No Apparent Injuries")
plt.ylabel("Number of Injuries")
plt.xlabel("Car Model")
plt.bar(filtered.index, values, color = colors)
plt.show()

values = filtered.loc[:, 'possible injury']
plt.xticks(rotation = 45, ha = 'right')
plt.title("Possible Injury")
plt.ylabel("Number of Injuries")
plt.xlabel("Car Model")
plt.bar(filtered.index, values, color = colors)
plt.show()
