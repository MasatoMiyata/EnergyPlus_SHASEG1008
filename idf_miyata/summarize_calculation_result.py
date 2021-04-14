#%%
import pandas as pd
import numpy as np

## 宮田作成ファイル
filename = "./idf_miyata/case600.csv"


name_dict = {
    "zone_name"   : "ZONE1",
    "wall_name_s" : "WALL_S",
    "wall_name_n" : "WALL_N",
    "wall_name_w" : "WALL_W",
    "wall_name_e" : "WALL_E",
    "roof_name"   : "ROOF",
    "window_name_1" : "WINDOW_S1",
    "window_name_2" : "WINDOW_S2"
}

## 小野さん作成ファイル
# filename = "./DesignBuilder/Case600.csv"

# name_dict = {
#     "zone_name"   : "BLOCK1:ZONE1",
#     "wall_name_s" : "BLOCK1:ZONE1_WALL_S",
#     "wall_name_n" : "BLOCK1:ZONE1_WALL_N",
#     "wall_name_w" : "BLOCK1:ZONE1_WALL_W",
#     "wall_name_e" : "BLOCK1:ZONE1_WALL_E",
#     "roof_name"   : "BLOCK1:ZONE1_ROOF_1_0_0",
# }

## AS140のファイル
# filename = "./docs/EnergyPlus-Std140TestSuites-InputFiles-v8.2/Case600_BESTEST.csv"

# name_dict = {
#     "zone_name"   : "ZONE ONE",
#     "wall_name_s" : "ZONE SURFACE SOUTH",
#     "wall_name_n" : "ZONE SURFACE NORTH",
#     "wall_name_w" : "ZONE SURFACE WEST",
#     "wall_name_e" : "ZONE SURFACE EAST",
#     "roof_name"   : "ZONE SURFACE ROOF",
# }


#%%
## データの読み込み

# 時刻ラベルを生成
dates = pd.date_range(start='1/1/2021 0:00:00', end='12/31/2021 23:00:00', freq='H')

# データの読み込み
data  = pd.read_csv(filepath_or_buffer=filename, sep=",", header=[0], encoding="cp932")

# 時刻ラベルをインデックスに指定（ csvファイルの時刻は 1〜24時で記載されており、datetime型として認識できない ）
data.index = dates
data.index.name = "data_hour"

# 確認
# print(data["WALL_S:Surface Outside Face Sunlit Area [m2](Hourly)"]["2021-01-01 7:00:00":"2021-01-01 17:00:00"])


# %%
#--------------------------------
# for Case 600
#--------------------------------

df_results = pd.DataFrame()

df_results["case600"] = pd.Series({

    "anual_heating_load" : np.sum( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000000,  # 年間の暖房負荷 [MWh/年]   1 Wh = 3600 J
    "anual_cooling_load" : np.sum( data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000000,  # 年間の冷房負荷 [MWh/年]
    "maximum_heating_load" : np.max( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000,  # 最大暖房負荷 [kW]
    "maximum_cooling_load" : np.max( data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000,  # 最大冷房負荷 [kW]
    "solar_radiation_N" : np.sum( data[ name_dict["wall_name_n"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000,  # 年間積算日射量（全天） [kWh/m2]
    "solar_radiation_E" : np.sum( data[ name_dict["wall_name_e"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000,  # 年間積算日射量（全天） [kWh/m2]
    "solar_radiation_W" : np.sum( data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000,  # 年間積算日射量（全天） [kWh/m2]
    "solar_radiation_S" : np.sum( data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000,  # 年間積算日射量（全天） [kWh/m2]
    "solar_radiation_H" : np.sum( data[ name_dict["roof_name"]   + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000,  # 年間積算日射量（全天） [kWh/m2]
    "solar_transitted"  : ( np.sum( data[ name_dict["window_name_1"] + ":Surface Window Transmitted Solar Radiation Rate [W](Hourly)"]) + \
                        np.sum( data[ name_dict["window_name_2"] + ":Surface Window Transmitted Solar Radiation Rate [W](Hourly)"]) ) /1000 / 12,   # 窓面透過日射量 [kWh/m2]
    "transmissivity_coefficient": 0
})

# 窓の日射透過係数
df_results["case600"]["transmissivity_coefficient"] = df_results["case600"]["solar_transitted"] / df_results["case600"]["solar_radiation_S"]

# 曇天日3/5の南面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_March_5_south_"+str(hh)] = data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"][hh]
df["case600"] = pd.Series(tmp)
df_results = df_results.append(df)

# 曇天日3/5の西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_March_5_west_"+str(hh)] = data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"][hh]
df["case600"] = pd.Series(tmp)
df_results = df_results.append(df)

# 晴天日7/27の南面・西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_July_27_south_"+str(hh)] = data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"][hh]
df["case600"] = pd.Series(tmp)
df_results = df_results.append(df)

# 曇天日7/27の西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_July_27_west_"+str(hh)] = data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"][hh]
df["case600"] = pd.Series(tmp)
df_results = df_results.append(df)


# 代表日1/4の冷暖房負荷
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["hourly_heatload_winter_"+str(hh)] = ( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"]["2021/1/4"][hh] - \
        data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "]["2021/1/4"][hh] ) /3600 /1000
df["case600"] = pd.Series(tmp)
df_results = df_results.append(df)

df_results.to_csv("集計データ.csv")


#--------------------------------
# for Case 600FF
#--------------------------------

# # 自然室温
# maximum_room_air_temperature = np.max( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
# print(f"自然室温 最大値 ℃ {maximum_room_air_temperature}")

# minimum_room_air_temperature = np.min( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
# print(f"自然室温 最小値 ℃ {minimum_room_air_temperature}")

# average_room_air_temperature = np.mean( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
# print(f"自然室温 平均値 ℃ {average_room_air_temperature}")


# # 代表日1/4の自然室温
# hourly_room_air_temperature = ( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021/1/4"] )
# print("--- 1/4 自然室温 ---")
# print(hourly_room_air_temperature)





# %%

## ラベルの一覧 （コピー用）
# "WALL_S:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WALL_S:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WALL_S:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "WALL_N:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WALL_N:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WALL_N:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "WALL_W:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WALL_W:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WALL_W:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "WALL_E:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WALL_E:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WALL_E:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "ROOF:Surface Outside Face Sunlit Area [m2](Hourly)"
# "ROOF:Surface Outside Face Sunlit Fraction [](Hourly)"
# "ROOF:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"

# "WINDOW_S1:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WINDOW_S1:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WINDOW_S1:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Solar Radiation Rate [W](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Beam Solar Radiation Rate [W](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Diffuse Solar Radiation Rate [W](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Solar Radiation Energy [J](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Beam Solar Radiation Energy [J](Hourly)"
# "WINDOW_S1:Surface Window Transmitted Diffuse Solar Radiation Energy [J](Hourly)"

# "WINDOW_S2:Surface Outside Face Sunlit Area [m2](Hourly)"
# "WINDOW_S2:Surface Outside Face Sunlit Fraction [](Hourly)"
# "WINDOW_S2:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Solar Radiation Rate [W](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Beam Solar Radiation Rate [W](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Diffuse Solar Radiation Rate [W](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Solar Radiation Energy [J](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Beam Solar Radiation Energy [J](Hourly)"
# "WINDOW_S2:Surface Window Transmitted Diffuse Solar Radiation Energy [J](Hourly)"
# "ZONE1:Zone Mean Air Temperature [C](Hourly)"
# "ZONE1:Zone Air System Sensible Heating Energy [J](Hourly)"
# "ZONE1:Zone Air System Sensible Cooling Energy [J](Hourly) " 
