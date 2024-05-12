import tkinter as tk
from tkinter import ttk
import webbrowser
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import geopandas as gpd


class UI:
    def __init__(self, map_creator):
        self.map_creator = map_creator
        self.root = tk.Tk()
        self.root.title("地図表示アプリ")

        self.frame_left = tk.Frame(self.root, width=200, height=600)
        self.frame_left.grid(row=0, column=0, sticky="ns")
        self.frame_right = tk.Frame(self.root, width=800, height=600)
        self.frame_right.grid(row=0, column=1, sticky="nsew")

        # Region Selection
        self.region_var = tk.StringVar(value='地域を選択')
        self.region_combobox = ttk.Combobox(self.frame_left, textvariable=self.region_var, values=['地域を選択'] + list(self.map_creator.regions.keys()))
        self.region_combobox.grid(row=0, column=0, padx=10, pady=10)
        self.region_combobox.bind("<<ComboboxSelected>>", self.update_prefecture_options)

        # Prefecture Selection
        self.prefecture_var = tk.StringVar(value='都道府県を選択')
        self.prefecture_combobox = ttk.Combobox(self.frame_left, textvariable=self.prefecture_var, values=['都道府県を選択'])
        self.prefecture_combobox.grid(row=1, column=0, padx=10, pady=10)

        # Show Map Button
        self.show_map_button = tk.Button(self.frame_left, text="地図を表示", command=self.show_map)
        self.show_map_button.grid(row=2, column=0, padx=10, pady=10)

        # # Background Map Selection
        # self.background_map_var = tk.StringVar()
        # self.background_map_combobox = ttk.Combobox(self.frame_left, textvariable=self.background_map_var, values=['Map1', 'Map2', 'Map3'])
        # self.background_map_combobox.grid(row=2, column=0, padx=10, pady=10)  # Use grid instead of pack

        # マーカー選択用コンボボックス
        self.marker_combobox = ttk.Combobox(self.frame_left, values=['コンビニ', '郵便局'])
        self.marker_combobox.grid(row=3, column=0, padx=10, pady=10)  # Corrected to use grid

        # データ分析のグラフを表示するキャンバス
        self.graph_canvas = tk.Canvas(self.root, width=800, height=200)
        self.graph_canvas.grid(row=1, column=1, sticky="nsew")

    def update_prefecture_options(self, event):
        if self.region_var.get() != '地域を選択':
            prefectures = self.map_creator.regions.get(self.region_var.get(), [])
            self.prefecture_combobox['values'] = ['都道府県を選択'] + prefectures
            self.prefecture_combobox.set('都道府県を選択')

    def get_center_coordinates(self, selected_prefecture):
        geojson_data = self.map_creator.geojson_data_ken  # Assuming this is a GeoDataFrame
        filtered_gdf = geojson_data[geojson_data['N03_001'] == selected_prefecture]
        center_lat = filtered_gdf.geometry.centroid.y.mean()
        center_lon = filtered_gdf.geometry.centroid.x.mean()
        return center_lat, center_lon, filtered_gdf


    def show_map(self):
        selected_prefecture = self.prefecture_var.get()
        if selected_prefecture != '都道府県を選択':
            center_lat, center_lon, filtered_gdf = self.get_center_coordinates(selected_prefecture)
            # Generate map HTML file
            map_filename = self.map_creator.create_map(selected_prefecture, filtered_gdf, center_lat, center_lon, self.map_creator.geojson_data_ken)
            # Display map in web browser
            webbrowser.open_new_tab(map_filename)
            # Optionally, display the map inside the application using a widget like a web view or an iframe if required



    def display_graph(self, event):
        # 選択されたマーカータイプを取得
        marker_type = self.marker_combobox.get()
        # ダミーデータの生成（実際には適切なデータソースからデータを取得する必要があります）
        x = np.linspace(0, 10, 100)
        y = np.sin(x) + np.random.normal(size=100) * 0.1  # サンプルとして正弦波にノイズを加えたデータを生成
    
        # プロットの作成
        fig, ax = plt.subplots()
        ax.plot(x, y, label=f'{marker_type}データ')
        ax.set_xlabel('X 軸')
        ax.set_ylabel('Y 軸')
        ax.legend()
        ax.grid(True)
    
        # グラフを一時ファイルに保存し、それをキャンバスに表示
        plt.savefig('/tmp/marker_data_graph.png')
        plt.close(fig)
        img = Image.open('/tmp/marker_data_graph.png')
        img_tk = ImageTk.PhotoImage(img)
        self.graph_canvas.create_image(0, 0, image=img_tk, anchor='nw')
        self.graph_canvas.image = img_tk  # 参照を保持して画像が表示され続けるようにする
        
    def run(self):
        self.root.mainloop()

# Assuming map_creator is an instance of MapCreator with regions and prefectures loaded
if __name__ == "__main__":
    import map_creator
    map_creator = map_creator.MapCreator()  # Ensure this is properly initialized with regions
    app = UI(map_creator)
    app.run()