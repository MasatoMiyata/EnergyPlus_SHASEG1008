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
    "1F廊下":"1F:01XCORRIDOR",
    "1Fロビー":"1F:02XLOBBY",
    "1FEVホール":"1F:03XEVHALL",
    "1F中央監視室":"1F:04XCNTRLMNTRNGRM",
    "1F更衣室1":"1F:05XDRESSING1",
    "1F更衣室2":"1F:06XDRESSING2",
    "1F休憩室":"1F:07XBREAKROOM",
    "1F自販機ｺｰﾅｰ":"1F:08XVENDING",
    "1F事務室1":"1F:09XOFFICE1",
    "1F事務室2":"1F:10XOFFICE2",
    "2-6F廊下":"2X6F:01XCORRIDOR",
    "2-6F自販機ｺｰﾅｰ":"2X6F:02XVENDING",
    "2-6FEVホール":"2X6F:03XEVHALL",
    "2-6F事務室1NP":"2X6F:04X1XOFFICENP",
    "2-6F事務室1NEP":"2X6F:04X2XOFFICENEP",
    "2-6F事務室1NWP":"2X6F:04X3XOFFICENWP",
    "2-6F事務室1NI":"2X6F:04X4XOFFICENI",
    "2-6F事務室2SP":"2X6F:05X1XOFFICESP",
    "2-6F事務室2SWP":"2X6F:05X2XOFFICESWP",
    "2-6F事務室2SI":"2X6F:05X3XOFFICESI",
    "7F廊下":"7F:01XCORRIDOR",
    "7F自販機ｺｰﾅｰ":"7F:02XVENDING",
    "7FEVホール":"7F:03XEVHALL",
    "7F事務室1":"7F:04XOFFICE1",
    "7F事務室2":"7F:05XOFFICE2",
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


for room_name in roomlist:

    fig = plt.figure(figsize=(14,7))
    plt.subplots_adjust(left=0.05, bottom=0.10, right=0.97, top=0.9, wspace=0.20, hspace=0.25)
    plt.subplot(111)
    plt.plot(data[roomlist[room_name] + ":Zone Mean Air Temperature [C](Hourly)"]) 
    plt.title(room_name)
    plt.grid()


plt.show()