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
filename = "./idf_miyata/CaseSRT.csv"

roomlist = {
    "Zone1":{
        "ID": "Zone1",
        "面積": 48.0,
        }
}

#-----------------------------
# データの読み込み
#-----------------------------

# 時刻ラベルを生成（15分毎）
dates = pd.date_range(start='1/1/2022 0:15:00', end='1/1/2023 0:00:00', freq='15T')

# CSVファイルの読み込み
data  = pd.read_csv(filepath_or_buffer=filename, sep=",", header=[0], encoding="cp932")

# 時刻ラベルをインデックスに指定（ csvファイルの時刻は 1〜24時で記載されており、datetime型として認識できない ）
data.index = dates
data.index.name = "data_hour"

for colunms_name in data.columns:
    if colunms_name[-1] == " ":  # EnergyPlusの出力項目名称の末尾になぜか空白が入ってしまう場合がある問題を解消
        print(colunms_name)
        data = data.rename(columns={colunms_name:colunms_name[:-1]})

# 確認
# print( data["ZONE1AIR:Zone Ideal Loads Zone Total Cooling Energy [J](TimeStep)"]["2022-01-04 07:00:00":"2022-01-04 13:00:00"] )


#-----------------------------------------------------------
# 集計
#-----------------------------------------------------------

temperature = "ZONE1:Zone Mean Air Temperature [C](TimeStep)"
humidity    = "ZONE1:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](TimeStep)"
Qh_sensible = "ZONE1AIR:Zone Ideal Loads Zone Sensible Heating Energy [J](TimeStep)"
Qh_latent   = "ZONE1AIR:Zone Ideal Loads Zone Latent Heating Energy [J](TimeStep)"
Qh_total    = "ZONE1AIR:Zone Ideal Loads Zone Total Heating Energy [J](TimeStep)"
Qc_sensible = "ZONE1AIR:Zone Ideal Loads Zone Sensible Cooling Energy [J](TimeStep)"
Qc_latent   = "ZONE1AIR:Zone Ideal Loads Zone Latent Cooling Energy [J](TimeStep)"
Qc_total    = "ZONE1AIR:Zone Ideal Loads Zone Total Cooling Energy [J](TimeStep)"

# "Environment:Site Outdoor Air Drybulb Temperature [C](Hourly)"
# "ZONE1:Zone Mean Air Temperature [C](Hourly)"
# "ZONE1:Zone Mean Air Humidity Ratio [kgWater/kgDryAir](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Sensible Heating Energy [J](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Latent Heating Energy [J](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Total Heating Energy [J](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Sensible Cooling Energy [J](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Latent Cooling Energy [J](Hourly)"
# "ZONE1AIR:Zone Ideal Loads Zone Total Cooling Energy [J](Hourly)"


data[ "顕熱負荷_J/15min" ] = data[ Qc_sensible ] - data[ Qh_sensible ]
data[ "潜熱負荷_J/15min" ] = data[ Qc_latent ] - data[ Qh_latent ]
data[ "顕熱負荷_W/m2" ] = data[ "顕熱負荷_J/15min" ] /roomlist["Zone1"]["面積"] / (15*60)
data[ "潜熱負荷_W/m2" ] = data[ "潜熱負荷_J/15min" ] /roomlist["Zone1"]["面積"] / (15*60)


#-----------------------------------------------------------
# 積算負荷、最大負荷の出力
#-----------------------------------------------------------

print( "---- 積算負荷・最大負荷 ----")

# 積算負荷 [MJ/m2年]
print( data[ data["顕熱負荷_J/15min" ] > 0 ]["顕熱負荷_J/15min" ].sum() / 1000000 /roomlist["Zone1"]["面積"])
print( data[ data["潜熱負荷_J/15min" ] > 0 ]["潜熱負荷_J/15min" ].sum() / 1000000 /roomlist["Zone1"]["面積"])
print( data[ data["顕熱負荷_J/15min" ] < 0 ]["顕熱負荷_J/15min" ].sum() / 1000000 /roomlist["Zone1"]["面積"])
print( data[ data["潜熱負荷_J/15min" ] < 0 ]["潜熱負荷_J/15min" ].sum() / 1000000 /roomlist["Zone1"]["面積"])

# 最大負荷 [W/m2]
print( data[ data["顕熱負荷_W/m2"] > 0 ]["顕熱負荷_W/m2"].max())
print( data[ data["潜熱負荷_W/m2"] > 0 ]["潜熱負荷_W/m2"].max())
print( data[ data["顕熱負荷_W/m2"] < 0 ]["顕熱負荷_W/m2"].min())
print( data[ data["潜熱負荷_W/m2"] < 0 ]["潜熱負荷_W/m2"].min())


#-----------------------------------------------------------
# 室温のグラフ
#-----------------------------------------------------------

fig = plt.figure(figsize=(10,7))
plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)
plt.subplot(411)
plt.plot(data[temperature]) 
plt.title("室温の変動: Zone1")
plt.ylabel("室温 [℃]")
plt.ylim([0,40])
plt.grid()

plt.subplot(412)
plt.plot(data[humidity]*1000) 
plt.title("絶対湿度の変動: Zone1")
plt.ylabel("絶対湿度 [g/kgDA]")
plt.ylim([0,25])
plt.grid()

plt.subplot(413)
plt.plot(data[Qc_sensible] /roomlist["Zone1"]["面積"] / (15*60), 'b')
plt.plot(data[Qh_sensible]*(-1)/roomlist["Zone1"]["面積"] / (15*60), 'r')
plt.title("顕熱負荷の変動: Zone1")
plt.ylabel("顕熱負荷 [W/㎡]")
plt.ylim([-300,200])
plt.grid()

plt.subplot(414)
plt.plot(data[ Qc_latent ]/roomlist["Zone1"]["面積"]/(15*60), 'b')
plt.plot(data[ Qh_latent ]*(-1)/roomlist["Zone1"]["面積"]/(15*60), 'r')
plt.title("潜熱負荷の変動: Zone1")
plt.ylabel("潜熱負荷 [W/㎡]")
plt.ylim([-300,200])
plt.grid()

plt.savefig("建物全体テスト_温湿度と熱負荷のグラフ_"+ "Zone1" +".png")



plt.show()