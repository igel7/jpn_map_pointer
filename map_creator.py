import folium
import os


class MapCreator:
    def __init__(self, geojson_data, geojson_data_ken, railroad_data, highway_data, convenience_data, post_office_data):
        # 現在のスクリプトのディレクトリを取得
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.geojson_data = geojson_data
        self.geojson_data_ken = geojson_data_ken
        self.railroad_data = railroad_data
        self.highway_data = highway_data
        self.convenience_data = convenience_data
        self.post_office_data = post_office_data
        self.regions = {
            '北海道・東北': ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
            '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
            '中部': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
            '近畿': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
            '中国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
            '四国': ['徳島県', '香川県', '愛媛県', '高知県'],
            '九州・沖縄': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
        }

    def create_map(self, selected_prefecture, filtered_gdf, center_lat, center_lon, geojson_data_ken):
        # とりあえず空の地図を作る（この上にレイヤーを載せていく）
        m = folium.Map(
            location=[center_lat, center_lon],
            tiles=None,  # No base tiles initially
            zoom_start=9,
            max_zoom=11,
            min_zoom=5,
            attr='blank',
            no_wrap=True
        )

        # Base map layer using relative path
        base_map_path = os.path.join(self.base_path, 'data', 'localmap', 'png', '{z}', '{x}', '{y}.png')
        folium.TileLayer(
            tiles='file:///' + base_map_path,  # Use file URI scheme
            name="普通の地図",
            attr="ry",
            max_zoom=11,
            min_zoom=5
        ).add_to(m)

        # Base map layer using relative path
        base_map_path = os.path.join(self.base_path, 'data', 'localmap', 'png_wh', '{z}', '{x}', '{y}.png')
        folium.TileLayer(
            tiles='file:///' + base_map_path,  # Use file URI scheme
            name="普通の地図",
            attr="ry",
            max_zoom=11,
            min_zoom=5
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

        folium.LayerControl().add_to(m)
        
        return m


# # デバッグ用
# map_creator = MapCreator()
# map_obj = map_creator.create_map('Tokyo', None, 35.6895, 139.6917, None)
# map_obj.save('output_map.html')  # Save the map to an HTML file for viewing



    def get_center_coordinates(self, selected_prefecture):
        filtered_gdf = self.geojson_data[self.geojson_data['N03_001'] == selected_prefecture]
        center_lat = filtered_gdf.geometry.centroid.y.mean()
        center_lon = filtered_gdf.geometry.centroid.x.mean()
        return center_lat, center_lon

    def create_legend(self, convenience_data, post_office_data):
        # ここで動的な凡例を生成するロジックを追加する
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 90px; background-color: white; border: 2px solid grey; z-index: 9999; padding: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4);">
        <h4>Legend</h4>
        """
        if 'convenience' in convenience_data:
            legend_html += '<div style="display: flex; align-items: center; gap: 10px;"><div style="width: 15px; height: 15px; background-color: blue; border-radius: 50%;"></div><span>コンビニ</span></div>'
        if 'post_office' in post_office_data:
            legend_html += '<div style="display: flex; align-items: center; gap: 10px;"><div style="width: 15px; height: 15px; background-color: red; border-radius: 50%;"></div><span>郵便局</span></div>'

        legend_html += "</div>"
        return legend_html
