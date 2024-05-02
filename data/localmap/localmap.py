# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 03:13:39 2024

@author: ryasu
"""
# from offline_folium import offline

import folium
import webbrowser
import os

os.chdir('C:\\Users/ryasu\\Desktop\\WPy64-31050\\notebooks\\folium\\localmap')

tileset = 'file:///C:/Users/ryasu/Desktop/WPy64-31050/notebooks/folium/localmap/png/{z}/{x}/{y}.png'
# tileset = 'C:\\Users\\ryasu\\Desktop\\WPy64-31050\\notebooks\\folium\\localmap\\png\\{z}\\{x}\\{y}.png'
# tileset = 'file:///C:\\Users\\ryasu\\Desktop\\WPy64-31050\\notebooks\\folium\\localmap\\png\\{z}\\{x}\\{y}.png'
m = folium.Map(tiles=tileset,
               location=[36.10315081987101, 138.07221931648996],
               zoom_start=5,max_zoom=11,min_zoom=5, 
               attr='Test',
               no_wrap=True)
# m = folium.Map(tiles=tileset,zoom_start=5,attr='Test',no_wrap=False)
m.save("local_map.html") # 地図をHTMLファイルとして保存
webbrowser.open("local_map.html") # 地図をウェブブラウザで表示


print(os.listdir("\\".join((folium.__file__).split('\\')[:-1])))
print("\\".join((folium.__file__).split("\\")[:-1]))
