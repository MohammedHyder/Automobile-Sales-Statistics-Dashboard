import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import requests 

# import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
# resp = await fetch(URL)
# text = io.BytesIO((await resp.arrayBuffer()).to_py())
resp = requests.get(URL)
text = resp.text

df = pd.read_csv(text)
print('Data downloaded and read into a dataframe!')
df.head()

df_rec = df[df['Recession'] == 1]

sales_by_city = df_rec.groupby('City')['Automobile_Sales'].sum().reset_index()

# base map centered on US 

map1 = folium.Map(location=[37.0902, -95.7129], zoom_start = 4)

# Create a choropleth layer using Folium
choropleth = folium.Choropleth(
        geo_data = 'us-states.json',
        data = sales_by_city, 
        columns=['City', 'Automobile_Sales'],
        key_on='feature.properties.name',
        fill_color = 'YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2, 
        legend_name = 'Automobile Sales during Recession'
).add_to(map1)

# add tooltips to choropleth layer 
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], labels=True)
)

# display map
map1