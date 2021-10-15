#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# グラフ文字化け対策
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams["font.size"] = 10

# ファイル名の指定
filename = "./idf_miyata/CaseWBT.csv"

roomlist = {
    "1F 廊下":{
        "ID": "1F:01XCORRIDOR",
        "面積": 163.5,
        },
    "1F ロビー":{
        "ID": "1F:02XLOBBY",
        "面積": 100.0,
        },
    "1F EVホール":{
        "ID": "1F:03XEVHALL",
        "面積": 12.0,
        },
    "1F 中央監視室":{
        "ID": "1F:04XCNTRLMNTRNGRM",
        "面積": 39.0,
        },
    "1F 更衣室1":{
        "ID": "1F:05XDRESSING1",
        "面積": 10.9,
        },
    "1F 更衣室2":{
        "ID": "1F:06XDRESSING2",
        "面積": 10.9,
        },
    "1F 休憩室":{
        "ID": "1F:07XBREAKROOM",
        "面積": 21.8,
        },
    "1F 自販機コーナー":{
        "ID": "1F:08XVENDING",
        "面積": 21.8,
        },
    "1F 事務室1":{
        "ID": "1F:09XOFFICE1",
        "面積": 366.8,
        },
    "1F 事務室2":{
        "ID": "1F:10XOFFICE2",
        "面積": 273.0,
        },
    "2-6F 廊下":{
        "ID": "2X6F:01XCORRIDOR",
        "面積": 144.0,
        },
    "2-6F 自販機コーナー":{
        "ID": "2X6F:02XVENDING",
        "面積": 21.8,
        },
    "2-6F EVホール":{
        "ID": "2X6F:03XEVHALL",
        "面積": 12.0,
        },
    "2-6F 事務室1 ペリメータ北":{
        "ID": "2X6F:04X1XOFFICENP",
        "面積": 187.5,
        },
    "2-6F 事務室1 ペリメータ北東":{
        "ID": "2X6F:04X2XOFFICENEP",
        "面積": 57.5,
        },
    "2-6F 事務室1 ペリメータ北西":{
        "ID": "2X6F:04X3XOFFICENWP",
        "面積": 57.5,
        },
    "2-6F 事務室1 インテリア":{
        "ID": "2X6F:04X4XOFFICENI",
        "面積": 292.5,
        },
    "2-6F 事務室2 ペリメータ南":{
        "ID": "2X6F:05X1XOFFICESP",
        "面積": 167.5,
        },
    "2-6F 事務室2 ペリメータ南西":{
        "ID": "2X6F:05X2XOFFICESWP",
        "面積": 57.5,
        },
    "2-6F 事務室2 インテリア":{
        "ID": "2X6F:05X3XOFFICESI",
        "面積": 279.0,
        },
    "7F 廊下":{
        "ID": "7F:01XCORRIDOR",
        "面積": 144.0,
        },
    "7F 自販機コーナー":{
        "ID": "7F:02XVENDING",
        "面積": 21.8,
        },
    "7F EVホール":{
        "ID": "7F:03XEVHALL",
        "面積": 12.0,
        },
    "7F 事務室1":{
        "ID": "7F:04XOFFICE1",
        "面積": 595.0,
        },
    "7F 事務室2":{
        "ID": "7F:05XOFFICE2",
        "面積": 504.0,
        }
}

# 時刻ラベルを生成
dates = pd.date_range(start='1/1/2021 0:00:00', end='12/31/2021 23:00:00', freq='H')

# データの読み込み
data  = pd.read_csv(filepath_or_buffer=filename, sep=",", header=[0], encoding="cp932")

# 時刻ラベルをインデックスに指定（ csvファイルの時刻は 1〜24時で記載されており、datetime型として認識できない ）
data.index = dates
data.index.name = "data_hour"

# 確認
# print(data[roomlist["1F事務室2"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-01-01 7:00:00":"2021-01-01 17:00:00"])

# 集計





# # 室温のグラフ
# for room_name in roomlist:

#     print(room_name)

#     fig = plt.figure(figsize=(14,7))
#     plt.subplots_adjust(left=0.07, bottom=0.10, right=0.97, top=0.9, wspace=0.20, hspace=0.25)
#     plt.subplot(211)
#     plt.plot(data[roomlist[room_name] + ":Zone Mean Air Temperature [C](Hourly)"]) 
#     plt.title("室温の変動: " +room_name)
#     plt.ylabel("室温 [℃]")
#     plt.ylim([5,35])
#     plt.grid()
#     plt.subplot(212)
#     plt.plot(data[roomlist[room_name] + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Cooling Energy [J](Hourly)"]/1000000, 'b')
#     plt.plot(data[roomlist[room_name] + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Heating Energy [J](Hourly)"]/1000000*(-1), 'r')
#     plt.title("熱負荷の変動: " +room_name)
#     plt.ylabel("負荷 [MJ]")
#     plt.grid()

# plt.show()