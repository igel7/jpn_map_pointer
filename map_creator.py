# -*- coding: utf-8 -*-
"""
Created on Wed May  1 01:39:43 2024

@author: ryasu
"""

import folium
import branca.colormap as cm
from shapely.geometry import Point
import pandas as pd
import geojson

class MapCreator:
    def __init__(self, geojson_data, geojson_data_ken, railroad_data, highway_data, convenience_data, post_office_data):
        self.geojson_data = geojson_data
        self.geojson_data_ken = geojson_data_ken
        self.railroad_data = railroad_data
        self.highway_data = highway_data
        self.convenience_data = convenience_data
        self.post_office_data = post_office_data
    
    def create_map(self, selected_prefecture, filtered_gdf, center_lat, center_lon, geojson_data_ken):
        # とりあえず空の地図を作る（この上にレイヤーを載せていく）
        m = folium.Map(tiles='', # タイルなし
                       location=[center_lat, center_lon],
                       zoom_start=9, max_zoom=11, min_zoom=5,
                       attr='blank',
                       no_wrap=True)

        # openstreetmap（画像の集積）
        folium.TileLayer(
            tiles='file:///C:/Users/ryasu/Desktop/WPy64-31050/projects/jpn_map_pointer/data/localmap/png/{z}/{x}/{y}.png',  
            name="普通の地図",
            attr="ry",
            max_zoom=11, min_zoom=5,
            overlay=False,
            control=True,
            show=True,
            styles={'background-color': 'white'}  # 背景色を白色に設定
        ).add_to(m)
        
        # 白地図（これも画像の集積）
        folium.TileLayer(
            tiles='file:///C:/Users/ryasu/Desktop/WPy64-31050/projects/jpn_map_pointer/data/localmap/png_wh/{z}/{x}/{y}.png',
            name="白地図",
            attr="ry",
            max_zoom=11, min_zoom=5,
            overlay=False,
            control=True,
            show=True,
            styles={'background-color': 'white'}  # 背景色を白色に設定
        ).add_to(m)
            
        # スクショ撮るときとかに使うことを想定して背景なしのレイヤーも入れておく
        folium.TileLayer(
            tiles='',  
            name="背景なし",
            attr="ry",
            max_zoom=11, min_zoom=5,
            overlay=False,
            control=True,
            show=True,
            styles={'background-color': 'white'}  # 背景色を白色に設定・・・しようとしたけどうまくいってない、原因不明
        ).add_to(m)
        
        
        # 人口密度レイヤーの作成
        self.create_population_density_layer(m, filtered_gdf, selected_prefecture)
        
        # 都道府県レイヤーの作成
        self.add_prefecture_boundary_layer(m, geojson_data_ken, selected_prefecture)
        
        # 市区町村レイヤーの作成
        self.add_municipal_boundaries_layer(m, filtered_gdf)
        
        # 道路データの追加
        self.add_railroad_and_highway(m, filtered_gdf)
        
        # コンビニと郵便局のマーカー追加
        self.add_convenience_and_post_office(m, selected_prefecture)
        
        # レイヤーコントロールを追加
        folium.LayerControl().add_to(m)
        
        return m
    
    def create_population_density_layer(self, m, filtered_gdf, selected_prefecture):
        # ポリゴン境界データのレイヤーを作成
        polygon_layer = folium.FeatureGroup(name="市区町村の人口密度")
        
        # 人口密度の最小値と最大値を計算
        min_density = filtered_gdf['density'].min()
        max_density = filtered_gdf['density'].max()
        
        # カラーマップを作成
        cmap = cm.LinearColormap(
            ['white', 'blue'],
            vmin=min_density,
            vmax=max_density,
            caption='人口密度'
        )
        
        # ポリゴン境界データのスタイル設定
        def style_function(feature):
            density = feature['properties'].get('density', None)
            if density is None:
                return {'color': 'black', 'weight': 1, 'fill': False}
            else:
                color = cmap(density)
                return {
                    'color': 'transparent',  # 境界線の色を透明に設定
                    'weight': 0, # 　境界の太さをゼロにしてある（境界線は別のレイヤーで設定するため）
                    'fill': True,
                    'fillColor': color,
                    'fill_opacity': 0.4
                }
        
        # GeoJSONデータを地図に追加
        geojson_object = folium.GeoJson(filtered_gdf, style_function=style_function)
        geojson_object.add_to(polygon_layer)
        
        # ポリゴンレイヤーを地図に追加
        polygon_layer.add_to(m)

    def add_prefecture_boundary_layer(self, m, geojson_data_ken, selected_prefecture):
        # 県レベルの境界レイヤーを作成
        filtered_gdf_ken = geojson_data_ken[geojson_data_ken['ADM1_JA'] == selected_prefecture]
        pref_boundary_layer = folium.FeatureGroup(name="指定都道府県の境界")
        # 境界線のスタイル設定
        def pref_boundary_style_function(feature):
            return {
                'color': 'blue',  # 境界線の色を黒に設定
                'weight': 2,  # 境界線の太さを設定
                'fill': False,  # 塗りつぶしなし
            }

        # GeoJSONデータを境界レイヤーに追加
        folium.GeoJson(
            filtered_gdf_ken,  # `geojson`モジュールを使用して境界をMultiPolygonで表示
            style_function=pref_boundary_style_function
        ).add_to(pref_boundary_layer)
        
        # 境界レイヤーを地図に追加
        pref_boundary_layer.add_to(m)   


    def add_municipal_boundaries_layer(self, m, filtered_gdf):
        # 市区町村の境界レイヤーを作成
        municipal_boundary_layer = folium.FeatureGroup(name="指定都道府県の境界（市区町村）")
        
        # 境界線のスタイル設定
        def boundary_style_function(feature):
            return {
                'color': 'blue',  # 境界線の色を黒色に設定
                'weight': 0.8,  # 境界線の太さを設定
                'fill': False,  # ポリゴンの塗りつぶしをしない
            }
        
        # GeoJSONデータを境界レイヤーに追加
        folium.GeoJson(filtered_gdf, style_function=boundary_style_function).add_to(municipal_boundary_layer)
        
        # 境界レイヤーを地図に追加
        municipal_boundary_layer.add_to(m)

    def add_railroad_and_highway(self, m, filtered_gdf):
        # 指定した都道府県のポリゴン境界を取得
        prefecture_polygon = filtered_gdf.unary_union
        
        # 高速道路データを指定した都道府県のポリゴン境界内にクリッピング
        kousoku_gdf_clipped = self.highway_data.clip(prefecture_polygon)
        # 鉄道路線データを指定した都道府県のポリゴン境界内にクリッピング
        tetsudo_gdf_clipped = self.railroad_data.clip(prefecture_polygon)
        
        # 高速道路データのレイヤーを作成
        kousoku_layer = folium.FeatureGroup(name="高速道路")
        
        # 高速道路のスタイル設定
        def kousoku_style_function(feature):
            return {
                'color': 'gray',
                'weight': 4,
            }
        
        # クリッピングした高速道路データをGeoJsonオブジェクトに追加
        folium.GeoJson(
            kousoku_gdf_clipped,
            style_function=kousoku_style_function
        ).add_to(kousoku_layer)
        kousoku_layer.add_to(m)
        
        # 鉄道路線データのレイヤーを作成
        tetsudo_layer = folium.FeatureGroup(name="鉄道")
        
        # 鉄道のスタイル設定
        def tetsudo_style_function(feature):
            return {
                'color': 'black',
                'weight': 4,
            }
        
        # クリッピングした鉄道路線データをGeoJsonオブジェクトに追加
        folium.GeoJson(
            tetsudo_gdf_clipped,
            style_function=tetsudo_style_function
        ).add_to(tetsudo_layer)
        tetsudo_layer.add_to(m)
        
    def add_convenience_and_post_office(self, m, selected_prefecture):
        # コンビニと郵便局のマーカーを地図に追加
        convenience_layer = folium.FeatureGroup(name="コンビニ")
        post_office_layer = folium.FeatureGroup(name="郵便局")
        
        # 指定した都道府県のコンビニデータをフィルタリング
        filtered_convenience_data = self.convenience_data[self.convenience_data['都道府県'] == selected_prefecture]
        
        # コンビニマーカーを追加
        for _, row in filtered_convenience_data.iterrows():
            # fY列もしくはfX列が空欄の場合は作業の対象外とする
            if pd.notna(row['fY']) and pd.notna(row['fX']):
                folium.CircleMarker(
                    location=[row['fY'], row['fX']],
                    radius=4,
                    color='blue',
                    weight=1.5,
                    fill=False,
                    fill_opacity=0.5
                ).add_to(convenience_layer)
        convenience_layer.add_to(m)
        
        # 指定した都道府県の郵便局データをフィルタリング
        filtered_post_office_data = self.post_office_data[self.post_office_data['都道府県'] == selected_prefecture]
        
        # 郵便局マーカーを追加
        for _, row in filtered_post_office_data.iterrows():
            # fY列もしくはfX列が空欄の場合は作業の対象外とする
            if pd.notna(row['fY']) and pd.notna(row['fX']):
                folium.CircleMarker(
                    location=[row['fY'], row['fX']],
                    radius=4,
                    color='red',
                    weight=1.5,
                    fill=False,
                    fill_opacity=0.5
                ).add_to(post_office_layer)
        post_office_layer.add_to(m)

