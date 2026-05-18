import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Load built-in world dataset
url = "https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_20m.zip"
states = gpd.read_file(url)

# Remove territories
#exclude = [
#    "Puerto Rico",
#    "Guam",
#    "American Samoa",
#    "Commonwealth of the Northern Mariana Islands",
#    "United States Virgin Islands"
#]

keep = [
    'AL','AZ','AR','CA','CO','CT','DE','FL','GA',
    'ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY',
    'DC'
]

# Filter for U.S.
#states = states[~states['NAME'].isin(exclude)]
continental_states = states[states["STUSPS"].isin(keep)]



# Plot
fig, ax = plt.subplots(figsize=(12,7))
continental_states.plot(ax=ax, facecolor='lightgreen', edgecolor='black', linewidth=0.8)

akax = fig.add_axes([0.1, 0.17, 0.2, 0.19])
akax.axis('off')
polygon = Polygon([(-170,50),(-170,72),(-140,72),(-140,50)])
alaska_gdf = states[states["STUSPS"]=='AK']
alaska_gdf.clip(polygon).plot(ax=akax)

hiax = fig.add_axes([0.22, 0.15, 0.24, 0.17])
hiax.axis('off')
hawaii_gdf = states[states["STUSPS"]=='HI']
hawaii_gdf.plot(ax=hiax)



ax.set_title('Map of the United States')
ax.set_axis_off()

plt.show()
