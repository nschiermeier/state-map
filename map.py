import json
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
cmap = plt.cm.get_cmap("tab20", len(years))
# Get all 20 colors, but skip indices 14 and 15 (They are gray, same as missing state)
all_colors = [cmap(i/20) for i in range(20) if i not in (14, 15)]
color_dict = {year: all_colors[i] for i, year in enumerate(years)}
merged["color"] = merged["YEAR"].map(color_dict)
merged["color"] = merged["color"].apply(lambda x: x if isinstance(x, tuple) else (0.85, 0.85, 0.85, 1.0))

# Just get continental?
# Plot
fig, ax = plt.subplots(figsize=(12,7))
merged.plot(color=merged["color"], ax=ax, edgecolor='black', linewidth=0.8)

# Add count of states / year, as well as remaining count
year_counts = df["YEAR"].dropna().astype(int).value_counts()
no_year_counts = df["YEAR"].isna().sum()

legend_patches = [
  mpatches.Patch(color=color_dict[yr], label=f"{yr} ({year_counts.get(yr, 0)})") for yr in years
]
legend_patches.append(mpatches.Patch(color=(0.85, 0.85, 0.85, 1.0), 
                      label=f"Not Visited \n({no_year_counts} Remaining)")
)

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
merged_ak["color"] = merged_ak["color"].apply(lambda x: x if isinstance(x, tuple) else (0.85, 0.85, 0.85, 1.0))
merged_ak.clip(polygon).plot(color=merged_ak.clip(polygon)["color"], ax=akax, edgecolor='black', linewidth=0.8)


hiax = fig.add_axes([0.22, 0.15, 0.24, 0.17])
hiax.axis('off')
hawaii_gdf = states[states["STUSPS"] == 'HI']
merged_hi = hawaii_gdf.merge(df, left_on="STUSPS", right_on="STATE", how="left")
merged_hi["color"] = merged_hi["YEAR"].dropna().astype(int).map(color_dict)
merged_hi["color"] = merged_hi["color"].apply(lambda x: x if isinstance(x, tuple) else (0.85, 0.85, 0.85, 1.0))
merged_hi.plot(color=merged_hi["color"], ax=hiax, edgecolor='black', linewidth=0.8)


ax.set_title('Map of the United States')
ax.set_axis_off()

plt.show()
