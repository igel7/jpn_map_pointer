# -*- coding: utf-8 -*-
"""
Created on Wed May  1 01:41:21 2024

@author: ryasu
"""

import tkinter as tk
from tkinter import ttk
import webbrowser
import folium

class UI:
    def __init__(self, map_creator):
        self.root = tk.Tk()
        self.root.title("地図アプリ")
        # self.data_loader = data_loader
        self.map_creator = map_creator
        # map_creatorからデータを取得
        self.geojson_data = map_creator.geojson_data
        self.geojson_data_ken = map_creator.geojson_data_ken
        self.railroad_data = map_creator.railroad_data
        self.highway_data = map_creator.highway_data
        self.convenience_data = map_creator.convenience_data
        self.post_office_data = map_creator.post_office_data
        # UIのウィジェットを作成
        self.create_widgets()
        # デバッグ用
        # print("geojson_data in UI:", self.geojson_data)
        # print("railroad_data in UI:", self.railroad_data)
        # print("highway_data in UI:", self.highway_data)
        # print("convenience_data in UI:", self.convenience_data)
        # print("post_office_data in UI:", self.post_office_data) 
        
    def create_widgets(self):
        # 地方と都道府県の対応を辞書で定義
        self.regions_prefectures = {
            '北海道・東北': ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
            '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
            '中部': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
            '近畿': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
            '中国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
            '四国': ['徳島県', '香川県', '愛媛県', '高知県'],
            '九州・沖縄': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
        }

        # 地方のプルダウンメニューの作成
        self.region_var = tk.StringVar()
        self.region_menu = ttk.Combobox(self.root, textvariable=self.region_var, values=list(self.regions_prefectures.keys()))
        self.region_menu.set("地方を選択してください")
        self.region_menu.bind('<<ComboboxSelected>>', self.on_region_select)
        self.region_menu.pack(pady=10)

        # 都道府県のプルダウンメニューの作成
        self.prefecture_var = tk.StringVar()
        self.prefecture_menu = ttk.Combobox(self.root, textvariable=self.prefecture_var)
        self.prefecture_menu.set("都道府県を選択してください")
        self.prefecture_menu.pack(pady=10)

        # ボタンの作成
        self.button = tk.Button(self.root, text="地図を表示", command=self.display_map)
        self.button.pack(pady=10)

    def on_region_select(self, event):
        # 地方が選択された際の処理
        selected_region = self.region_var.get()
        print("geojson_data in UI:", selected_region) # デバッグ用
        # 選択された地方に属する都道府県のリストを取得
        self.prefecture_menu['values'] = self.regions_prefectures[selected_region]
        self.prefecture_menu.set("都道府県を選択してください")

    def display_map(self):
        # 地図を表示する
        selected_prefecture = self.prefecture_var.get().strip()
        print("selected_prefecture in UI:", selected_prefecture) # デバッグ用        
        # print("geojson_data in display_map:", self.geojson_data) # デバッグ用
        # 中心座標の取得
        center_lat, center_lon, filtered_gdf = self.get_center_coordinates(self.geojson_data, selected_prefecture)
        geojson_data_ken = self.geojson_data_ken

        # 地図の作成
        m = self.map_creator.create_map(selected_prefecture, filtered_gdf, center_lat, center_lon, geojson_data_ken)
        # 凡例を作成
        legend_html = """
        <div style="
            position: fixed;
            bottom: 50px;
            left: 50px;
            z-index: 9999;
            background-color: rgba(255, 255, 255, 1.0);
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 1.0);
            font-size: 12px;
        ">
            <h4></h4>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 15px; height: 15px; background-color: blue; border-radius: 50%;"></div>
                <span>コンビニ</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 15px; height: 15px; background-color: red; border-radius: 50%;"></div>
                <span>郵便局</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 30px; height: 4px; background-color: gray;"></div>
                <span>高速道路</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 30px; height: 4px; background-color: black;"></div>
                <span>鉄道</span>
            </div>
        </div>
        """
    
        # 地図に凡例を追加
        m.get_root().html.add_child(folium.Element(legend_html))    
        # 地図をファイルとして保存
        map_filename = f"{selected_prefecture}_map.html"
        m.save(map_filename)

        # 地図をブラウザで表示
        webbrowser.open(map_filename)

    def get_center_coordinates(self, geojson_data, selected_prefecture):
        # print("geojson_data in get_center_coordinates:", geojson_data) # デバッグ用
        # print("selected_prefecture:", selected_prefecture) # デバッグ用
        # 都道府県の中心座標を取得する
        # selected_prefecture = '鳥取県'
        filtered_gdf = geojson_data[geojson_data['N03_001'] == selected_prefecture]
        center_lat = filtered_gdf.geometry.centroid.y.mean()
        # center_lat = 35.38078428066388 #デバッグ用
        center_lon = filtered_gdf.geometry.centroid.x.mean()
        # center_lon = 133.73639807083106 #デバッグ用
        return center_lat, center_lon, filtered_gdf

    def run(self):
        # アプリケーションを実行
        self.root.mainloop()
