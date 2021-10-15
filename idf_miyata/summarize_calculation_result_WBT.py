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
    "1F_廊下":{
        "ID": "1F:01XCORRIDOR",
        "面積": 163.5,
        },
    "1F_ロビー":{
        "ID": "1F:02XLOBBY",
        "面積": 100.0,
        },
    "1F_EVホール":{
        "ID": "1F:03XEVHALL",
        "面積": 12.0,
        },
    "1F_中央監視室":{
        "ID": "1F:04XCNTRLMNTRNGRM",
        "面積": 39.0,
        },
    "1F_更衣室1":{
        "ID": "1F:05XDRESSING1",
        "面積": 10.9,
        },
    "1F_更衣室2":{
        "ID": "1F:06XDRESSING2",
        "面積": 10.9,
        },
    "1F_休憩室":{
        "ID": "1F:07XBREAKROOM",
        "面積": 21.8,
        },
    "1F_自販機コーナー":{
        "ID": "1F:08XVENDING",
        "面積": 21.8,
        },
    "1F_事務室1":{
        "ID": "1F:09XOFFICE1",
        "面積": 366.8,
        },
    "1F_事務室2":{
        "ID": "1F:10XOFFICE2",
        "面積": 273.0,
        },
    "2-6F_廊下":{
        "ID": "2X6F:01XCORRIDOR",
        "面積": 144.0,
        },
    "2-6F_自販機コーナー":{
        "ID": "2X6F:02XVENDING",
        "面積": 21.8,
        },
    "2-6F_EVホール":{
        "ID": "2X6F:03XEVHALL",
        "面積": 12.0,
        },
    "2-6F_事務室1_ペリメータ北":{
        "ID": "2X6F:04X1XOFFICENP",
        "面積": 187.5,
        },
    "2-6F_事務室1_ペリメータ北東":{
        "ID": "2X6F:04X2XOFFICENEP",
        "面積": 57.5,
        },
    "2-6F_事務室1_ペリメータ北西":{
        "ID": "2X6F:04X3XOFFICENWP",
        "面積": 57.5,
        },
    "2-6F_事務室1_インテリア":{
        "ID": "2X6F:04X4XOFFICENI",
        "面積": 292.5,
        },
    "2-6F_事務室2_ペリメータ南":{
        "ID": "2X6F:05X1XOFFICESP",
        "面積": 167.5,
        },
    "2-6F_事務室2_ペリメータ南西":{
        "ID": "2X6F:05X2XOFFICESWP",
        "面積": 57.5,
        },
    "2-6F_事務室2_インテリア":{
        "ID": "2X6F:05X3XOFFICESI",
        "面積": 279.0,
        },
    "7F_廊下":{
        "ID": "7F:01XCORRIDOR",
        "面積": 144.0,
        },
    "7F_自販機コーナー":{
        "ID": "7F:02XVENDING",
        "面積": 21.8,
        },
    "7F_EVホール":{
        "ID": "7F:03XEVHALL",
        "面積": 12.0,
        },
    "7F_事務室1":{
        "ID": "7F:04XOFFICE1",
        "面積": 595.0,
        },
    "7F_事務室2":{
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

for colunms_name in data.columns:
    if colunms_name[-1] == " ":  # EnergyPlusの出力項目名称の末尾になぜか空白が入ってしまう場合がある問題を解消
        print(colunms_name)
        data = data.rename(columns={colunms_name:colunms_name[:-1]})


# # 確認
# # print(data[roomlist["1F事務室2"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-01-01 7:00:00":"2021-01-01 17:00:00"])

# 集計

# 積算負荷（冷房顕熱）

for room_name in roomlist:

    print( "----" + room_name + "----")

    if "2-6F" in room_name:
        Multiplier = 5
    else:
        Multiplier = 1

    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"].sum() / 1000000 )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"].sum() / 1000000 )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"].sum() / 1000000*(-1) )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"].sum() / 1000000*(-1) )

    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Energy [J](Hourly)"].sum() / 1000000 /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Energy [J](Hourly)"].sum() / 1000000 /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Energy [J](Hourly)"].sum() / 1000000*(-1) /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Energy [J](Hourly)"].sum() / 1000000*(-1) /roomlist[room_name]["面積"]/Multiplier)

    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"].max() / 1000 )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"].max() / 1000 )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"].max() / 1000*(-1) )
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"].max() / 1000*(-1) )

    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"].max() /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"].max() /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"].max() *(-1) /roomlist[room_name]["面積"]/Multiplier)
    print( data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"].max() *(-1) /roomlist[room_name]["面積"]/Multiplier)


# 室温のグラフ
for room_name in roomlist:

    print(room_name)

    fig = plt.figure(figsize=(10,7))
    plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
    plt.subplot(311)
    plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]) 
    plt.title("室温の変動: " +room_name)
    plt.ylabel("室温 [℃]")
    plt.ylim([5,35])
    plt.grid()

    plt.subplot(312)
    plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]*1000) 
    plt.title("絶対湿度の変動: " +room_name)
    plt.ylabel("絶対湿度 [g/kgDA]")
    plt.ylim([0,20])
    plt.grid()
    
    plt.subplot(313)
    plt.plot(data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Cooling Rate [W](Hourly)"]/roomlist[room_name]["面積"], 'b')
    plt.plot(data[roomlist[room_name]["ID"]  + " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Heating Rate [W](Hourly)"]*(-1)/roomlist[room_name]["面積"], 'r')
    plt.title("熱負荷の変動: " +room_name)
    plt.ylabel("負荷 [W/㎡]")
    plt.grid()

    plt.savefig("CaseWBT_温湿度と熱負荷_"+ room_name +".png")

# plt.show()