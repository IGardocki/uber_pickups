# imports
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC') #puts in a title

#sets DATE_COLUMN to 'date/time'
DATE_COLUMN = 'date/time'
#gives url to pull from
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz') 

#caches data
@st.cache
#defines load_data function
def load_data(nrows): 
    #reads data from the url
    data = pd.read_csv(DATA_URL, nrows=nrows)
    #creates anon function to convert to lowercase string 
    lowercase = lambda x: str(x).lower()
    #renames data with lowercase function
    data.rename(lowercase, axis='columns', inplace=True)
    #converts string to datetime type
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done (using @st.cache)!')

#checks if checkbox with text 'Show raw data is checked' and shows raw data if so
if st.checkbox('Show raw data'):
    #creates subheader that reads 'Raw Data'
    st.subheader('Raw data')
    #writes the data
    st.write(data)

#creates another subheader
st.subheader('Number of pickups by hour')

#sets hist_values to a numpy histogram by hour (.dt.hour)
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# uses streamlit's .bar_chart to plot hist_values
st.bar_chart(hist_values)

st.subheader('Map of all pickups') #another subheader

st.map(data) #creates a map! This is cool. Need to figure out exactly how this works. I assume it just pulls in the lat/longs given in data, but not exactly sure.

# UPDATE: from the st.map docs, the df you're plotting must have columns called 'lat', 'lon', 'latitude', or 'longitude'.

#sets the hr we want to look at
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h 
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] #filter the df so we only look at that hr
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)