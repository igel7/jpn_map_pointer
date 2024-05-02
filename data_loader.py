# -*- coding: utf-8 -*-
"""
Created on Wed May  1 01:38:42 2024

@author: ryasu
"""

import geopandas as gpd
import pandas as pd
import feather

class DataLoader:
    def __init__(self, geojson_path, geojson_ken_path, railroad_path, highway_path, convenience_path, post_office_path):
        self.geojson_path = geojson_path
        self.geojson_ken_path = geojson_ken_path
        self.railroad_path = railroad_path
        self.highway_path = highway_path
        self.convenience_path = convenience_path
        self.post_office_path = post_office_path
        
    def load_geojson(self):
        return gpd.read_file(self.geojson_path)
    
    def load_geojson_ken(self):
        return gpd.read_file(self.geojson_ken_path)
    
    def load_railroad(self):
        return gpd.read_file(self.railroad_path)
    
    def load_highway(self):
        return gpd.read_file(self.highway_path)
    
    def load_convenience(self):
        return feather.read_dataframe(self.convenience_path)
    
    def load_post_office(self):
        return feather.read_dataframe(self.post_office_path)
