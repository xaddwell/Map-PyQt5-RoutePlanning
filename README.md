# Map-PyQt5-RoutePlanning

实验任务（实验题目、目的）
Implement a shortest path algorithm and apply it to the national railway system.
以全国主要城市为图的顶点, 铁路连接为图的边, 距离作为加权, 设计完成一个最短路径自动查找系统. 输入为出发城市和目标城市, 输出为最短路径和距离.

实现思路
在研究、挖掘GPS位置数据、轨迹数据的过程中，地理信息的可视化展示是非常关键的一步。
folium是js上著名的地理信息可视化库leaflet.js为Python提供的接口，通过它，我们可以通过在Python端编写代码操纵数据，来调用leaflet的相关功能，基于内建的osm或自行获取的osm资源和地图原件进行地理信息内容的可视化，以及制作优美的可交互地图。
folium.map数:https://python-visualization.github.io/folium/modules.html#module-folium.map
　　location：tuple或list类型输入，用于控制初始地图中心点的坐标，格式为(纬度，经度)或[纬度，经度]，默认为None
　　width：int型或str型，int型时，传入的是地图宽度的像素值；str型时，传入的是地图宽度的百分比，形式为'xx%'。默认为'100%'
　　height：控制地图的高度，格式同width
　　tiles：str型，用于控制绘图调用的地图样式，默认为'OpenStreetMap'，也有一些其他的内建地图样式；也可以传入'None'来绘制一个没有风格的朴素地图，或传入一个URL来使用其它的自选osm
              可选的样式包括：
                 ”OpenStreetMap”
                 ”Stamen Terrain”, “Stamen Toner”, “Stamen Watercolor”
                 ”CartoDB positron”, “CartoDB dark_matter”
                 ”Mapbox Bright”, “Mapbox Control Room” (Limited zoom)
                 ”Cloudmade” (Must pass API key)
                 ”Mapbox” (Must pass API key)
　　max_zoom：int型，控制地图可以放大程度的上限，默认为18
　　attr：str型，当在tiles中使用自选URL内的osm时使用，用于给自选osm命名
　　control_scale：bool型，控制是否在地图上添加比例尺，默认为False即不添加
　　no_touch：bool型，控制地图是否禁止接受来自设备的触控事件譬如拖拽等，默认为False，即不禁止
Heatmap Parameters
data (list of points of the form [lat, lng] or [lat, lng, weight]) – The points you want to plot. You can also provide a numpy.array of shape (n,2) or (n,3).
name (string, default None) – The name of the Layer, as it will appear in LayerControls.
min_opacity (default 1.) – The minimum opacity the heat will start at.
max_zoom (default 18) – Zoom level where the points reach maximum intensity (as intensity scales with zoom), equals maxZoom of the map by default
max_val (float, default 1.) – Maximum point intensity
radius (int, default 25) – Radius of each “point” of the heatmap
blur (int, default 15) – Amount of blur
gradient (dict, default None) – Color gradient config. e.g. {0.4: ‘blue’, 0.65: ‘lime’, 1: ‘red’}
overlay (bool, default True) – Adds the layer as an optional overlay (True) or the base layer (False).
control (bool, default True) – Whether the Layer will be included in LayerControls.
show (bool, default True) – Whether the layer will be shown on opening (only for overlays).

使用的库
from PyQt5 import QtCore, QtGui, QtWidgets,QtWebEngineWidgets
import io,sys,folium
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np
import json
import pickle
import requests
from geopy.distance import geodesic
### 主要靠api实现

### 有条件搜索：起点，终点，中间节点，出行方式
 ![2](https://user-images.githubusercontent.com/72803316/126330826-246c0bee-1967-4aaf-9adc-24343ee7dbe8.png)

显示：全长距离，总预计耗时，备忘录会搜索路线指示
沿科华南路向南行驶368米直行进入隧道
沿科华南路向南行驶360米向右前方行驶进入匝道
沿科华南路出口途径科华南路向南行驶1.7千米右转
沿锦悦东路途径锦悦西路向西行驶528米右转
向北行驶24米到达目的地
总时间6938.45分钟
 
### 可以自己单击标注点，并且显示经纬度
 
### 可以将该次路线打开（.pkl）格式，或者自己命名保存
![3](https://user-images.githubusercontent.com/72803316/126331036-9045b25c-483b-4802-a0de-a4897da2a87e.png)

### 特殊功能：增加了打开网页的功能，上网，浏览网页，方便查询信息
 ![4](https://user-images.githubusercontent.com/72803316/126331020-0a116c2a-183e-4b7c-96e7-217b19bacffd.png)

### 可以娱乐玩小游戏
![6](https://user-images.githubusercontent.com/72803316/126331101-f1c3de86-49e0-4b36-a994-6fbc88678168.png)

 
### 提示：需要点击特殊按钮才能打开网页功能


