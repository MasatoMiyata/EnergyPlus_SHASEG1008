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
    "1F 廊下":"1F:01XCORRIDOR",
    "1F ロビー":"1F:02XLOBBY",
    "1F EVホール":"1F:03XEVHALL",
    "1F 中央監視室":"1F:04XCNTRLMNTRNGRM",
    "1F 更衣室1":"1F:05XDRESSING1",
    "1F 更衣室2":"1F:06XDRESSING2",
    "1F 休憩室":"1F:07XBREAKROOM",
    "1F 自販機コーナー":"1F:08XVENDING",
    "1F 事務室1":"1F:09XOFFICE1",
    "1F 事務室2":"1F:10XOFFICE2",
    "2-6F 廊下":"2X6F:01XCORRIDOR",
    "2-6F 自販機コーナー":"2X6F:02XVENDING",
    "2-6F EVホール":"2X6F:03XEVHALL",
    "2-6F 事務室1 ペリメータ北":"2X6F:04X1XOFFICENP",
    "2-6F 事務室1 ペリメータ北東":"2X6F:04X2XOFFICENEP",
    "2-6F 事務室1 ペリメータ北西":"2X6F:04X3XOFFICENWP",
    "2-6F 事務室1 インテリア":"2X6F:04X4XOFFICENI",
    "2-6F 事務室2 ペリメータ南":"2X6F:05X1XOFFICESP",
    "2-6F 事務室2 ペリメータ南西":"2X6F:05X2XOFFICESWP",
    "2-6F 事務室2 インテリア":"2X6F:05X3XOFFICESI",
    "7F 廊下":"7F:01XCORRIDOR",
    "7F 自販機コーナー":"7F:02XVENDING",
    "7F EVホール":"7F:03XEVHALL",
    "7F 事務室1":"7F:04XOFFICE1",
    "7F 事務室2":"7F:05XOFFICE2",
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

# 室温のグラフ
for room_name in roomlist:

    print(room_name)

    fig = plt.figure(figsize=(14,7))
    plt.subplots_adjust(left=0.07, bottom=0.10, right=0.97, top=0.9, wspace=0.20, hspace=0.25)
    plt.subplot(211)
    plt.plot(data[roomlist[room_name] + ":Zone Mean Air Temperature [C](Hourly)"]) 
    plt.title("室温の変動: " +room_name)
    plt.ylabel("室温 [℃]")
    plt.ylim([5,35])
    plt.grid()
    plt.subplot(212)
    plt.plot(data[roomlist[room_name] + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Cooling Energy [J](Hourly)"]/1000000, 'b')
    plt.plot(data[roomlist[room_name] + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Heating Energy [J](Hourly)"]/1000000*(-1), 'r')
    plt.title("熱負荷の変動: " +room_name)
    plt.ylabel("負荷 [MJ]")
    plt.grid()

plt.show()