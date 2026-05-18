import json
import math
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import pandas
from shapely.geometry import Polygon

states_csv = "state_map_data.csv"
df = pandas.read_csv(states_csv)

# Load built-in world dataset
url = "https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_20m.zip"
states = gpd.read_file(url)

keep = [
    'AL','AZ','AR','CA','CO','CT','DE','FL','GA',
    'ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY',
    'DC'
]

# Filter for continental U.S.
continental_states = states[states["STUSPS"].isin(keep)]

# combine gdf with year data
merged = continental_states.merge(df, left_on="STUSPS", right_on="STATE", how="left")

# get all the years and create a color map for them. If year is NA, then set it's color to gray.
years = sorted(df["YEAR"].dropna().unique().astype(int))
# Create custom colormap that can be expanded if need be, and also doesn't have gray
tab20_no_gray = [
  "#1f77b4", "#aec7e8",  # blue pair
  "#ff7f0e", "#ffbb78",  # orange pair
  "#2ca02c", "#98df8a",  # green pair
  "#d62728", "#ff9896",  # red pair
  "#9467bd", "#c5b0d5",  # purple pair
  "#8c564b", "#c49c94",  # brown pair
  "#e377c2", "#f7b6d2",  # pink pair
  # skipping grays (14, 15)
  "#bcbd22", "#dbdb8d",  # yellow-green pair
  "#17becf", "#9edae5",  # cyan pair
]
color_dict = {year: tab20_no_gray[i] for i, year in enumerate(years)}
merged["color"] = merged["YEAR"].map(color_dict)
merged["color"] = merged["color"].apply(lambda x: x if x is not None and not (isinstance(x, float) and math.isnan(x)) else (0.85, 0.85, 0.85, 1.0))

# Plot
fig, ax = plt.subplots(figsize=(12,7))
merged.plot(color=merged["color"], ax=ax, edgecolor='black', linewidth=0.8)

# Hatch layer for airport states
airport_states = merged[merged["AIRPORT"]==1]
airport_states.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=0.8, hatch='///')

# Add count of states / year, as well as remaining count
year_counts = df["YEAR"].dropna().astype(int).value_counts()
no_year_counts = df["YEAR"].isna().sum()

legend_patches = [
  mpatches.Patch(color=color_dict[yr], label=f"{yr} ({year_counts.get(yr, 0)})") for yr in years
]
legend_patches.append(mpatches.Patch(color=(0.85, 0.85, 0.85, 1.0), 
                      label=f"Not Visited \n({no_year_counts} Remaining)")
)
legend_patches.append(mpatches.Patch(facecolor='white', edgecolor='black', hatch='///', label="Airport Only"))

ax.legend(handles=legend_patches,
          title="Year",
          bbox_to_anchor = (0.95, 1),
          loc="upper left"
)

akax = fig.add_axes([0.1, 0.17, 0.2, 0.19])
akax.axis('off')
polygon = Polygon([(-170,50),(-170,72),(-140,72),(-140,50)])
alaska_gdf = states[states["STUSPS"] == 'AK']
merged_ak = alaska_gdf.merge(df, left_on="STUSPS", right_on="STATE", how="left")
merged_ak["color"] = merged_ak["YEAR"].dropna().astype(int).map(color_dict)
merged_ak["color"] = merged_ak["color"].apply(lambda x: x if x is not None and not (isinstance(x, float) and math.isnan(x)) else (0.85, 0.85, 0.85, 1.0))
merged_ak.clip(polygon).plot(color=merged_ak.clip(polygon)["color"], ax=akax, edgecolor='black', linewidth=0.8)


hiax = fig.add_axes([0.22, 0.15, 0.24, 0.17])
hiax.axis('off')
hawaii_gdf = states[states["STUSPS"] == 'HI']
merged_hi = hawaii_gdf.merge(df, left_on="STUSPS", right_on="STATE", how="left")
merged_hi["color"] = merged_hi["YEAR"].dropna().astype(int).map(color_dict)
merged_hi["color"] = merged_hi["color"].apply(lambda x: x if x is not None and not (isinstance(x, float) and math.isnan(x)) else (0.85, 0.85, 0.85, 1.0))
merged_hi.plot(color=merged_hi["color"], ax=hiax, edgecolor='black', linewidth=0.8)


ax.set_title('Map of U.S. States I\'ve Visited, by Year ')
ax.set_axis_off()

plt.show()
