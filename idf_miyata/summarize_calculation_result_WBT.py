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
        "階数": 1,
        },
    "1F_ロビー":{
        "ID": "1F:02XLOBBY",
        "面積": 100.0,
        "階数": 1,
        },
    "1F_EVホール":{
        "ID": "1F:03XEVHALL",
        "面積": 12.0,
        "階数": 1,
        },
    "1F_中央監視室":{
        "ID": "1F:04XCNTRLMNTRNGRM",
        "面積": 39.0,
        "階数": 1,
        },
    "1F_更衣室1":{
        "ID": "1F:05XDRESSING1",
        "面積": 10.9,
        "階数": 1,
        },
    "1F_更衣室2":{
        "ID": "1F:06XDRESSING2",
        "面積": 10.9,
        "階数": 1,
        },
    "1F_休憩室":{
        "ID": "1F:07XBREAKROOM",
        "面積": 21.8,
        "階数": 1,
        },
    "1F_自販機コーナー":{
        "ID": "1F:08XVENDING",
        "面積": 21.8,
        "階数": 1,
        },
    "1F_事務室1":{
        "ID": "1F:09XOFFICE1",
        "面積": 366.8,
        "階数": 1,
        },
    "1F_事務室2":{
        "ID": "1F:10XOFFICE2",
        "面積": 273.0,
        "階数": 1,
        },
    "2-6F_廊下":{
        "ID": "2X6F:01XCORRIDOR",
        "面積": 144.0,
        "階数": 5,
        },
    "2-6F_自販機コーナー":{
        "ID": "2X6F:02XVENDING",
        "面積": 21.8,
        "階数": 5,
        },
    "2-6F_EVホール":{
        "ID": "2X6F:03XEVHALL",
        "面積": 12.0,
        "階数": 5,
        },
        
    "2-6F_事務室1_ペリメータ北":{
        "ID": "2X6F:04X1XOFFICENP",
        "面積": 187.5,
        "階数": 5,
        },
    "2-6F_事務室1_ペリメータ北東":{
        "ID": "2X6F:04X2XOFFICENEP",
        "面積": 57.5,
        "階数": 5,
        },
    "2-6F_事務室1_ペリメータ北西":{
        "ID": "2X6F:04X3XOFFICENWP",
        "面積": 57.5,
        "階数": 5,
        },
    "2-6F_事務室1_インテリア":{
        "ID": "2X6F:04X4XOFFICENI",
        "面積": 292.5,
        "階数": 5,
        },

    "2-6F_事務室2_ペリメータ南":{
        "ID": "2X6F:05X1XOFFICESP",
        "面積": 167.5,
        "階数": 5,
        },
    "2-6F_事務室2_ペリメータ南西":{
        "ID": "2X6F:05X2XOFFICESWP",
        "面積": 57.5,
        "階数": 5,
        },
    "2-6F_事務室2_インテリア":{
        "ID": "2X6F:05X3XOFFICESI",
        "面積": 279.0,
        "階数": 5,
        },

    "7F_廊下":{
        "ID": "7F:01XCORRIDOR",
        "面積": 144.0,
        "階数": 1,
        },
    "7F_自販機コーナー":{
        "ID": "7F:02XVENDING",
        "面積": 21.8,
        "階数": 1,
        },
    "7F_EVホール":{
        "ID": "7F:03XEVHALL",
        "面積": 12.0,
        "階数": 1,
        },
    "7F_事務室1":{
        "ID": "7F:04XOFFICE1",
        "面積": 595.0,
        "階数": 1,
        },
    "7F_事務室2":{
        "ID": "7F:05XOFFICE2",
        "面積": 504.0,
        "階数": 1,
        }
}

#-----------------------------
# データの読み込み
#-----------------------------

# 時刻ラベルを生成
dates = pd.date_range(start='12/1/2021 1:00:00', end='1/1/2023 0:00:00', freq='H')
# dates = pd.date_range(start='1/1/2021 1:00:00', end='1/1/2023 0:00:00', freq='H')

# CSVファイルの読み込み
data  = pd.read_csv(filepath_or_buffer=filename, sep=",", header=[0], encoding="cp932")

# 時刻ラベルをインデックスに指定（ csvファイルの時刻は 1〜24時で記載されており、datetime型として認識できない ）
data.index = dates
data.index.name = "data_hour"

for colunms_name in data.columns:
    if colunms_name[-1] == " ":  # EnergyPlusの出力項目名称の末尾になぜか空白が入ってしまう場合がある問題を解消
        print(colunms_name)
        data = data.rename(columns={colunms_name:colunms_name[:-1]})

# # 確認
# # print(data[roomlist["1F事務室2"] + ":Zone Mean Air Temperature [C](Hourly)"]["2022-01-01 7:00:00":"2022-01-01 17:00:00"])

# 最後の一年のデータを抽出
data = data["2022-01-01 0:00:00":"2023-01-01 0:00:00"]


#-----------------------------------------------------------
# 集計
#-----------------------------------------------------------

temperature             = ":Zone Mean Air Temperature [C](Hourly)"
humidity                = ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"

sensible_cooling_rate_W = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"
sensible_heating_rate_W = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"
latent_cooling_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"
latent_heating_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"

total_cooling_rate_W    = " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Cooling Rate [W](Hourly)"
total_heating_rate_W    = " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Heating Rate [W](Hourly)"

sensible_cooling_energy_J = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Energy [J](Hourly)"
sensible_heating_energy_J = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Energy [J](Hourly)"
latent_cooling_energy_J   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Energy [J](Hourly)"
latent_heating_energy_J   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Energy [J](Hourly)"


for room_name in roomlist:

    data[ room_name + "_顕熱負荷_W" ] = data[roomlist[room_name]["ID"] + sensible_cooling_rate_W] - data[roomlist[room_name]["ID"] + sensible_heating_rate_W]
    data[ room_name + "_潜熱負荷_W" ] = data[roomlist[room_name]["ID"] + latent_cooling_rate_W]   - data[roomlist[room_name]["ID"] + latent_heating_rate_W]

    data[ room_name + "_顕熱負荷_J" ] = data[roomlist[room_name]["ID"] + sensible_cooling_energy_J] - data[roomlist[room_name]["ID"] + sensible_heating_energy_J]
    data[ room_name + "_潜熱負荷_J" ] = data[roomlist[room_name]["ID"] + latent_cooling_energy_J]   - data[roomlist[room_name]["ID"] + latent_heating_energy_J]


    # 全熱負荷（単純な積算）
    data[ room_name + "_全熱負荷_W" ] = data[ room_name + "_顕熱負荷_W" ] + data[ room_name + "_潜熱負荷_W" ]
    data[ room_name + "_全熱負荷_J" ] = data[ room_name + "_顕熱負荷_J" ] + data[ room_name + "_潜熱負荷_J" ]

    # 床面積あたりの負荷
    data[ room_name + "_顕熱負荷_W/m2" ] = data[ room_name + "_顕熱負荷_W" ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"]
    data[ room_name + "_潜熱負荷_W/m2" ] = data[ room_name + "_潜熱負荷_W" ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"]
    data[ room_name + "_全熱負荷_W/m2" ] = data[ room_name + "_全熱負荷_W" ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"]

#-----------------------------------------------------------
# 建物全体の全熱負荷
#-----------------------------------------------------------

data["建物全体_全熱負荷_J"] = 0
data["建物全体_顕熱負荷_W"] = 0
data["建物全体_潜熱負荷_W"] = 0
total_floor_area = 0

for room_name in roomlist:

    data["建物全体_全熱負荷_J"] += data[room_name + "_全熱負荷_J" ]
    data["建物全体_顕熱負荷_W"] += data[room_name + "_顕熱負荷_W" ]
    data["建物全体_潜熱負荷_W"] += data[room_name + "_潜熱負荷_W" ]
    total_floor_area += (roomlist[room_name]["面積"] * roomlist[room_name]["階数"])


#-----------------------------------------------------------
# 全熱負荷が最大となる日
#-----------------------------------------------------------

# 冷房負荷
print("---- 最大負荷が出現する日時（冷房） ---- ")
print(data[ data["建物全体_全熱負荷_J"] > 0 ]["建物全体_全熱負荷_J"].idxmax())   # 冷房負荷の最大
for room_name in roomlist:
    print( data[ data[room_name + "_全熱負荷_J" ] > 0 ][room_name + "_全熱負荷_J" ].idxmax() )   # 冷房負荷の最大

# 暖房負荷
print("---- 最大負荷が出現する日時（暖房） ---- ")
print(data[ data["建物全体_全熱負荷_J"] < 0 ]["建物全体_全熱負荷_J"].idxmin())   # 暖房負荷の最大
for room_name in roomlist:
    print( data[ data[room_name + "_全熱負荷_J" ] < 0 ][room_name + "_全熱負荷_J" ].idxmin() )   # 暖房負荷の最大



#-----------------------------------------------------------
# 積算負荷、最大負荷の出力
#-----------------------------------------------------------

print("---- 積算負荷、最大負荷 ---- ")

# 積算負荷 [MWh]
print( data[ data["建物全体_顕熱負荷_W" ] > 0 ]["建物全体_顕熱負荷_W"].sum() / 1000000  )  # 冷房顕熱
print( data[ data["建物全体_潜熱負荷_W" ] > 0 ]["建物全体_潜熱負荷_W"].sum() / 1000000  )  # 冷房顕熱
print( data[ data["建物全体_顕熱負荷_W" ] < 0 ]["建物全体_顕熱負荷_W"].sum() / 1000000  )  # 冷房顕熱
print( data[ data["建物全体_潜熱負荷_W" ] < 0 ]["建物全体_潜熱負荷_W"].sum() / 1000000  )  # 冷房顕熱

# 積算負荷 [MJ/m2年]
print( data[ data["建物全体_顕熱負荷_W" ] > 0 ]["建物全体_顕熱負荷_W"].sum() * 3600 / 1000000 /total_floor_area )  # 冷房顕熱
print( data[ data["建物全体_潜熱負荷_W" ] > 0 ]["建物全体_潜熱負荷_W"].sum() * 3600 / 1000000 /total_floor_area )  # 冷房顕熱
print( data[ data["建物全体_顕熱負荷_W" ] < 0 ]["建物全体_顕熱負荷_W"].sum() * 3600 / 1000000 /total_floor_area )  # 冷房顕熱
print( data[ data["建物全体_潜熱負荷_W" ] < 0 ]["建物全体_潜熱負荷_W"].sum() * 3600 / 1000000 /total_floor_area )  # 冷房顕熱

index_cooling_max = data[ data["建物全体_全熱負荷_J"] > 0 ]["建物全体_全熱負荷_J"].idxmax()
index_heating_max = data[ data["建物全体_全熱負荷_J"] < 0 ]["建物全体_全熱負荷_J"].idxmin()

print(data["建物全体_顕熱負荷_W"][ index_cooling_max ] /1000)
print(data["建物全体_潜熱負荷_W"][ index_cooling_max ] /1000)
print(data["建物全体_顕熱負荷_W"][ index_heating_max ] /1000)
print(data["建物全体_潜熱負荷_W"][ index_heating_max ] /1000)
print(data["建物全体_顕熱負荷_W"][ index_cooling_max ] /total_floor_area)
print(data["建物全体_潜熱負荷_W"][ index_cooling_max ] /total_floor_area)
print(data["建物全体_顕熱負荷_W"][ index_heating_max ] /total_floor_area)
print(data["建物全体_潜熱負荷_W"][ index_heating_max ] /total_floor_area)

for room_name in roomlist:

    print("----" + room_name + "----")

    # 積算負荷 [MWh]
    print( data[ data[room_name + "_顕熱負荷_W" ] > 0 ][room_name + "_顕熱負荷_W" ].sum() / 1000000  )   # 冷房顕熱
    print( data[ data[room_name + "_潜熱負荷_W" ] > 0 ][room_name + "_潜熱負荷_W" ].sum() / 1000000  )   # 冷房潜熱
    print( data[ data[room_name + "_顕熱負荷_W" ] < 0 ][room_name + "_顕熱負荷_W" ].sum() / 1000000  )   # 暖房顕熱
    print( data[ data[room_name + "_潜熱負荷_W" ] < 0 ][room_name + "_潜熱負荷_W" ].sum() / 1000000  )   # 暖房潜熱

    # 積算負荷 [MJ/m2年]
    print( data[ data[room_name + "_顕熱負荷_J" ] > 0 ][room_name + "_顕熱負荷_J" ].sum() / 1000000 /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[ data[room_name + "_潜熱負荷_J" ] > 0 ][room_name + "_潜熱負荷_J" ].sum() / 1000000 /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[ data[room_name + "_顕熱負荷_J" ] < 0 ][room_name + "_顕熱負荷_J" ].sum() / 1000000 /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[ data[room_name + "_潜熱負荷_J" ] < 0 ][room_name + "_潜熱負荷_J" ].sum() / 1000000 /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])

    # 全熱負荷が最大となる日の特定
    index_cooling_max = data[ data[room_name + "_全熱負荷_J" ] > 0 ][room_name + "_全熱負荷_J" ].idxmax()
    index_heating_max = data[ data[room_name + "_全熱負荷_J" ] < 0 ][room_name + "_全熱負荷_J" ].idxmin()

    # 最大負荷 [kW]
    print( data[room_name + "_顕熱負荷_W"][ index_cooling_max ] / 1000  )
    print( data[room_name + "_潜熱負荷_W"][ index_cooling_max ] / 1000  )
    print( data[room_name + "_顕熱負荷_W"][ index_heating_max ] / 1000  )
    print( data[room_name + "_潜熱負荷_W"][ index_heating_max ] / 1000  )

    # 最大負荷 [W/m2]
    print( data[room_name + "_顕熱負荷_W" ][ index_cooling_max ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[room_name + "_潜熱負荷_W" ][ index_cooling_max ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[room_name + "_顕熱負荷_W" ][ index_heating_max ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])
    print( data[room_name + "_潜熱負荷_W" ][ index_heating_max ] /roomlist[room_name]["面積"]/roomlist[room_name]["階数"])


# 保存
data.to_csv("建物全体テスト_全データ.csv", encoding="cp932")


#-----------------------------------------------------------
# 全ての室の時系列負荷 （CSVに出力）
#-----------------------------------------------------------

csvdata_building_total = pd.DataFrame([])

for room_name in roomlist: 
    csvdata_building_total = csvdata_building_total.append( data[ room_name + "_顕熱負荷_W" ] )

for room_name in roomlist: 
    csvdata_building_total = csvdata_building_total.append( data[ room_name + "_潜熱負荷_W" ] )

for room_name in roomlist: 
    csvdata_building_total = csvdata_building_total.append( data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"] )

for room_name in roomlist: 
    csvdata_building_total = csvdata_building_total.append( data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]*1000 )

csvdata_building_total.T.to_csv("建物全体テスト_負荷_温湿度データ.csv", encoding="cp932")

#-----------------------------------------------------------
# 基準階の事務室の時系列負荷 （CSVに出力）
#-----------------------------------------------------------

csvdata = pd.DataFrame([], columns=[
    "2-6F_事務室1_ペリメータ北_顕熱", "2-6F_事務室1_ペリメータ北東_顕熱", "2-6F_事務室1_ペリメータ北西_顕熱", "2-6F_事務室1_インテリア_顕熱",
    "2-6F_事務室2_ペリメータ南_顕熱", "2-6F_事務室2_ペリメータ南西_顕熱", "2-6F_事務室2_インテリア_顕熱", 
    "2-6F_事務室1_ペリメータ北_潜熱", "2-6F_事務室1_ペリメータ北東_潜熱", "2-6F_事務室1_ペリメータ北西_潜熱", "2-6F_事務室1_インテリア_潜熱",
    "2-6F_事務室2_ペリメータ南_潜熱", "2-6F_事務室2_ペリメータ南西_潜熱", "2-6F_事務室2_インテリア_潜熱",
    "2-6F_事務室1_ペリメータ北_室温", "2-6F_事務室1_ペリメータ北東_室温", "2-6F_事務室1_ペリメータ北西_室温", "2-6F_事務室1_インテリア_室温",
    "2-6F_事務室2_ペリメータ南_室温", "2-6F_事務室2_ペリメータ南西_室温", "2-6F_事務室2_インテリア_室温", 
    "2-6F_事務室1_ペリメータ北_湿度", "2-6F_事務室1_ペリメータ北東_湿度", "2-6F_事務室1_ペリメータ北西_湿度", "2-6F_事務室1_インテリア_湿度",
    "2-6F_事務室2_ペリメータ南_湿度", "2-6F_事務室2_ペリメータ南西_湿度", "2-6F_事務室2_インテリア_湿度", 
    ])

for room_name in roomlist:

    if "事務室" in room_name and "2-6F" in room_name:

        tmpdata = data[ room_name + "_顕熱負荷_W/m2" ]["2022-01-04 0:00:00":"2022-01-05 1:00:00"]
        tmpdata = tmpdata.append(data[ room_name + "_顕熱負荷_W/m2" ]["2022-04-05 0:00:00":"2022-04-06 1:00:00"] )
        tmpdata = tmpdata.append(data[ room_name + "_顕熱負荷_W/m2" ]["2022-07-18 0:00:00":"2022-07-19 1:00:00"] )
        tmpdata = tmpdata.append(data[ room_name + "_顕熱負荷_W/m2" ]["2022-11-1 0:00:00":"2022-11-2 1:00:00"] )

        csvdata[room_name + "_顕熱"] = tmpdata

        tmpdata = data[ room_name + "_潜熱負荷_W/m2" ]["2022-01-04 0:00:00":"2022-01-05 1:00:00"]
        tmpdata = tmpdata.append(data[ room_name + "_潜熱負荷_W/m2" ]["2022-04-05 0:00:00":"2022-04-06 1:00:00"] )
        tmpdata = tmpdata.append(data[ room_name + "_潜熱負荷_W/m2" ]["2022-07-18 0:00:00":"2022-07-19 1:00:00"] )
        tmpdata = tmpdata.append(data[ room_name + "_潜熱負荷_W/m2" ]["2022-11-1 0:00:00":"2022-11-2 1:00:00"] )

        csvdata[room_name + "_潜熱"] = tmpdata

        tmpdata = data[ roomlist[room_name]["ID"] + temperature ]["2022-01-04 0:00:00":"2022-01-05 1:00:00"]
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + temperature ]["2022-04-05 0:00:00":"2022-04-06 1:00:00"] )
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + temperature ]["2022-07-18 0:00:00":"2022-07-19 1:00:00"] )
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + temperature ]["2022-11-1 0:00:00":"2022-11-2 1:00:00"] )

        csvdata[room_name + "_室温"] = tmpdata

        tmpdata = data[ roomlist[room_name]["ID"] + humidity ]["2022-01-04 0:00:00":"2022-01-05 1:00:00"]
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + humidity ]["2022-04-05 0:00:00":"2022-04-06 1:00:00"] )
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + humidity ]["2022-07-18 0:00:00":"2022-07-19 1:00:00"] )
        tmpdata = tmpdata.append(data[ roomlist[room_name]["ID"] + humidity ]["2022-11-1 0:00:00":"2022-11-2 1:00:00"] )

        csvdata[room_name + "_湿度"] = tmpdata

        csvdata.to_csv("建物全体テスト_代表日データ.csv", encoding="cp932")


#-----------------------------------------------------------
# 室温のグラフ (png)
#-----------------------------------------------------------

for room_name in roomlist:

    if "事務室" in room_name and "2-6F" in room_name:

        print( "----" + room_name + "----")

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()
        
        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_"+ room_name +".png")


        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([15,25])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2022-01-04 0:00:00":"2022-01-07 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_01月"+ room_name +".png")


        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2022-04-05 0:00:00":"2022-04-08 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_04月"+ room_name +".png")

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2022-07-18 0:00:00":"2022-07-21 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_07月"+ room_name +".png")

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2022-11-1 0:00:00":"2022-11-4 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_11月"+ room_name +".png")

# plt.show()