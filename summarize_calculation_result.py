#%%
import pandas as pd
import numpy as np

## 宮田作成ファイル
# filename = "./results/case600/case600.csv"
# filename = "./results/case600FF/case600FF.csv"

# name_dict = {
#     "zone_name"   : "ZONE1",
#     "wall_name_s" : "WALL_S",
#     "wall_name_n" : "WALL_N",
#     "wall_name_w" : "WALL_W",
#     "wall_name_e" : "WALL_E",
#     "roof_name"   : "ROOF",
# }

## 小野さん作成ファイル
filename = "./DesignBuilder/Case600.csv"

name_dict = {
    "zone_name"   : "BLOCK1:ZONE1",
    "wall_name_s" : "BLOCK1:ZONE1_WALL_S",
    "wall_name_n" : "BLOCK1:ZONE1_WALL_N",
    "wall_name_w" : "BLOCK1:ZONE1_WALL_W",
    "wall_name_e" : "BLOCK1:ZONE1_WALL_E",
    "roof_name"   : "BLOCK1:ZONE1_ROOF_1_0_0",
}


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
# for Case 600

# 年間の暖房負荷 [MWh/年]
# 1 Wh = 3600 J
anual_heating_load = np.sum( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000000
print(f"年間暖房負荷 MWh {anual_heating_load}")

# 年間の冷房負荷 [MWh/年]
anual_cooling_load = np.sum( data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000000
print(f"年間冷房負荷 MWh {anual_cooling_load}")

# 最大暖房負荷 [kW]
maximum_heating_load = np.max( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000
print(f"最大暖房負荷 kW {maximum_heating_load}")

# 最大冷房負荷 [kW]
maximum_cooling_load = np.max( data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000
print(f"最大冷房負荷 kW {maximum_cooling_load}")

# 年間積算日射量（全天） [kWh/m2]
solar_radiation_N = np.sum( data[ name_dict["wall_name_n"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_E = np.sum( data[ name_dict["wall_name_e"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_W = np.sum( data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_S = np.sum( data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_H = np.sum( data[ name_dict["roof_name"]   + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000

print(f"年間積算日射量（全天）北 kWh/m2 {solar_radiation_N}")
print(f"年間積算日射量（全天）東 kWh/m2 {solar_radiation_E}")
print(f"年間積算日射量（全天）西 kWh/m2 {solar_radiation_W}")
print(f"年間積算日射量（全天）南 kWh/m2 {solar_radiation_S}")
print(f"年間積算日射量（全天）水平 kWh/m2 {solar_radiation_H}")

# 曇天日3/5の南面・西面日射量 [Wh/m2]
print("--- 3/5 南面 ---")
print(data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"])
print("--- 3/5 西面 ---")
print(data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"])

# 晴天日7/27の南面・西面日射量 [Wh/m2]
print("--- 7/27 南面 ---")
print(data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"])
print("--- 7/27 西面 ---")
print(data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"])

# 代表日1/4の冷暖房負荷
hourly_heatload_winter = ( \
    data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"]["2021/1/4"] - \
    data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "]["2021/1/4"] ) /3600 /1000

print("--- 1/4 冷暖房負荷 ---")
print(hourly_heatload_winter)


# 自然室温
maximum_room_air_temperature = np.max( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
print(f"自然室温 最大値 ℃ {maximum_room_air_temperature}")

minimum_room_air_temperature = np.min( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
print(f"自然室温 最小値 ℃ {minimum_room_air_temperature}")

average_room_air_temperature = np.mean( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
print(f"自然室温 平均値 ℃ {average_room_air_temperature}")


# 代表日1/4の自然室温
hourly_room_air_temperature = ( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021/1/4"] )
print("--- 1/4 自然室温 ---")
print(hourly_room_air_temperature)





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
