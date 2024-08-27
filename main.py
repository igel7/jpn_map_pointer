# -*- coding: utf-8 -*-
"""
Created on Wed May  1 01:43:48 2024

@author: ryasu
"""

# Load packages
print('Loading Packages...')
from data_loader import DataLoader
from map_creator import MapCreator
from ui import UI

# # for debug
# import os
# os.chdir('C:\\Users\\ryasu\\Desktop\\WPy64-31050\\notebooks\\folium')

# path to data files
geojson_path = "data/gdf.geojson"
geojson_ken_path = "data/gdf_ken.geojson"
railroad_path = "data/tetsudo/N02-22_RailroadSection.shp"
highway_path = "data/douro/N06-22_HighwaySection.shp"
convenience_path = "data/df_convenience.feather"
post_office_path = "data/df_post_office.feather"

# make instance of data_loader
data_loader = DataLoader(geojson_path, geojson_ken_path, railroad_path, highway_path, convenience_path, post_office_path)

# Load data
print('Loading geoJSON data...')
geojson_data = data_loader.load_geojson()
geojson_data_ken = data_loader.load_geojson_ken()
print('Loading ShapeFile data...')
railroad_data = data_loader.load_railroad()
highway_data = data_loader.load_highway()
print('Loading feather data...')
convenience_data = data_loader.load_convenience()
post_office_data = data_loader.load_post_office()

# make instance of MapCreator
map_creator = MapCreator(geojson_data, geojson_data_ken, railroad_data, highway_data, convenience_data, post_office_data)


# Make instance for UI and start the app
ui = UI(map_creator)
ui.run()
