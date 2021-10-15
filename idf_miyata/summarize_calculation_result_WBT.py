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
dates = pd.date_range(start='1/1/2021 1:00:00', end='1/1/2022 0:00:00', freq='H')

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

temperature             = ":Zone Mean Air Temperature [C](Hourly)"
humidity                = ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"
sensible_cooling_rate_W = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"
sensible_heating_rate_W = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"
latent_cooling_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"
latent_heating_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"
total_cooling_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Cooling Rate [W](Hourly)"
total_heating_rate_W   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Total Heating Rate [W](Hourly)"

sensible_cooling_energy_J = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Cooling Rate [W](Hourly)"
sensible_heating_energy_J = " IDEAL LOADS AIR:Zone Ideal Loads Zone Sensible Heating Rate [W](Hourly)"
latent_cooling_energy_J   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Cooling Rate [W](Hourly)"
latent_heating_energy_J   = " IDEAL LOADS AIR:Zone Ideal Loads Zone Latent Heating Rate [W](Hourly)"

# for room_name in roomlist:

#     print( "----" + room_name + "----")

#     if "2-6F" in room_name:
#         Multiplier = 5
#     else:
#         Multiplier = 1

#     print( data[roomlist[room_name]["ID"] + sensible_cooling_rate_W].sum() / 1000000 )
#     print( data[roomlist[room_name]["ID"] + latent_cooling_rate_W].sum() / 1000000 )
#     print( data[roomlist[room_name]["ID"] + sensible_heating_rate_W].sum() / 1000000*(-1) )
#     print( data[roomlist[room_name]["ID"] + latent_heating_rate_W].sum() / 1000000*(-1) )
#     print( data[roomlist[room_name]["ID"] + sensible_cooling_energy_J].sum() / 1000000 /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + latent_cooling_energy_J].sum() / 1000000 /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + sensible_heating_energy_J].sum() / 1000000*(-1) /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + latent_heating_energy_J].sum() / 1000000*(-1) /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + sensible_cooling_rate_W].max() / 1000 )
#     print( data[roomlist[room_name]["ID"] + latent_cooling_rate_W].max() / 1000 )
#     print( data[roomlist[room_name]["ID"] + sensible_heating_rate_W].max() / 1000*(-1) )
#     print( data[roomlist[room_name]["ID"] + latent_heating_rate_W].max() / 1000*(-1) )
#     print( data[roomlist[room_name]["ID"] + sensible_cooling_rate_W].max() /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + latent_cooling_rate_W].max() /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + sensible_heating_rate_W].max() *(-1) /roomlist[room_name]["面積"]/Multiplier)
#     print( data[roomlist[room_name]["ID"] + latent_heating_rate_W].max() *(-1) /roomlist[room_name]["面積"]/Multiplier)


# 基準階の事務室の時系列負荷
for room_name in roomlist:

    if "事務室" in room_name and "2-6F" in room_name:

        print( "----" + room_name + "----")

        Multiplier = 5

        data[ roomlist[room_name]["ID"] + " sensible_heat_load" ] = \
            data[roomlist[room_name]["ID"] + sensible_cooling_rate_W] /roomlist[room_name]["面積"]/Multiplier + \
            data[roomlist[room_name]["ID"] + sensible_heating_rate_W] *(-1) /roomlist[room_name]["面積"]/Multiplier

        data[ roomlist[room_name]["ID"] + " latent_heat_load" ] = \
            data[roomlist[room_name]["ID"] + latent_cooling_rate_W] /roomlist[room_name]["面積"]/Multiplier + \
            data[roomlist[room_name]["ID"] + latent_heating_rate_W] *(-1) /roomlist[room_name]["面積"]/Multiplier

        output_sensible_data = data[ roomlist[room_name]["ID"] + " sensible_heat_load" ]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]
        output_sensible_data = output_sensible_data.append(data[ roomlist[room_name]["ID"] + " sensible_heat_load" ]["2021-04-05 0:00:00":"2021-04-06 1:00:00"] )
        output_sensible_data = output_sensible_data.append(data[ roomlist[room_name]["ID"] + " sensible_heat_load" ]["2021-07-18 0:00:00":"2021-07-19 1:00:00"] )
        output_sensible_data = output_sensible_data.append(data[ roomlist[room_name]["ID"] + " sensible_heat_load" ]["2021-11-11 0:00:00":"2021-11-12 1:00:00"] )

        output_sensible_data.to_csv("建物全体テスト_代表日_顕熱負荷_"+ room_name + ".csv", encoding="cp932")

        output_latent_data = data[ roomlist[room_name]["ID"] + " latent_heat_load" ]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]
        output_latent_data = output_latent_data.append(data[ roomlist[room_name]["ID"] + " latent_heat_load" ]["2021-04-05 0:00:00":"2021-04-06 1:00:00"] )
        output_latent_data = output_latent_data.append(data[ roomlist[room_name]["ID"] + " latent_heat_load" ]["2021-07-18 0:00:00":"2021-07-19 1:00:00"] )
        output_latent_data = output_latent_data.append(data[ roomlist[room_name]["ID"] + " latent_heat_load" ]["2021-11-11 0:00:00":"2021-11-12 1:00:00"] )

        output_latent_data.to_csv("建物全体テスト_代表日_潜熱負荷_"+ room_name + ".csv", encoding="cp932")

        output_temperature_data = data[ roomlist[room_name]["ID"] + temperature ]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]
        output_temperature_data = output_temperature_data.append(data[ roomlist[room_name]["ID"] + temperature ]["2021-04-05 0:00:00":"2021-04-06 1:00:00"] )
        output_temperature_data = output_temperature_data.append(data[ roomlist[room_name]["ID"] + temperature ]["2021-07-18 0:00:00":"2021-07-19 1:00:00"] )
        output_temperature_data = output_temperature_data.append(data[ roomlist[room_name]["ID"] + temperature ]["2021-11-11 0:00:00":"2021-11-12 1:00:00"] )

        output_temperature_data.to_csv("建物全体テスト_代表日_室温_"+ room_name + ".csv", encoding="cp932")

        output_humidity_data = data[ roomlist[room_name]["ID"] + humidity ]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]
        output_humidity_data = output_humidity_data.append(data[ roomlist[room_name]["ID"] + humidity ]["2021-04-05 0:00:00":"2021-04-06 1:00:00"] )
        output_humidity_data = output_humidity_data.append(data[ roomlist[room_name]["ID"] + humidity ]["2021-07-18 0:00:00":"2021-07-19 1:00:00"] )
        output_humidity_data = output_humidity_data.append(data[ roomlist[room_name]["ID"] + humidity ]["2021-11-11 0:00:00":"2021-11-12 1:00:00"] )

        output_humidity_data.to_csv("建物全体テスト_代表日_湿度_"+ room_name + ".csv", encoding="cp932")



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
    plt.plot(data[roomlist[room_name]["ID"]  + total_cooling_rate_W]/roomlist[room_name]["面積"], 'b')
    plt.plot(data[roomlist[room_name]["ID"]  + total_heating_rate_W]*(-1)/roomlist[room_name]["面積"], 'r')
    plt.title("熱負荷の変動: " +room_name)
    plt.ylabel("負荷 [W/㎡]")
    plt.grid()

    plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_"+ room_name +".png")


    if "事務室" in room_name and "2-6F" in room_name:

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2021-01-04 0:00:00":"2021-01-05 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_01月"+ room_name +".png")


        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2021-04-05 0:00:00":"2021-04-06 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_04月"+ room_name +".png")

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2021-07-18 0:00:00":"2021-07-19 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_07月"+ room_name +".png")

        fig = plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
        plt.subplot(411)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]) 
        plt.title("室温の変動: " +room_name)
        plt.ylabel("室温 [℃]")
        plt.ylim([5,35])
        plt.grid()

        plt.subplot(412)
        plt.plot(data[roomlist[room_name]["ID"] + ":Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]*1000) 
        plt.title("絶対湿度の変動: " +room_name)
        plt.ylabel("絶対湿度 [g/kgDA]")
        plt.ylim([0,20])
        plt.grid()
        
        plt.subplot(413)
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_cooling_rate_W]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + sensible_heating_rate_W]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("顕熱負荷の変動: " +room_name)
        plt.ylabel("顕熱負荷 [W/㎡]")
        plt.grid()

        plt.subplot(414)
        plt.plot(data[roomlist[room_name]["ID"]  + latent_cooling_rate_W]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]/roomlist[room_name]["面積"], 'b')
        plt.plot(data[roomlist[room_name]["ID"]  + latent_heating_rate_W]["2021-11-11 0:00:00":"2021-11-12 1:00:00"]*(-1)/roomlist[room_name]["面積"], 'r')
        plt.title("潜熱負荷の変動: " +room_name)
        plt.ylabel("潜熱負荷 [W/㎡]")
        plt.grid()

        plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_代表日_11月"+ room_name +".png")

# plt.show()