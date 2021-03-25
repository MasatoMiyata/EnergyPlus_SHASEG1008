#%%
import pandas as pd
import numpy as np

filename = "./results/case600/case600.csv"

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


# %%
# for Case 600

# 年間の暖房負荷 [MWh/年]
# 1 Wh = 3600 J
anual_heating_load = np.sum( data["ZONE1:Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000000
print(f"年間暖房負荷 MWh {anual_heating_load}")

# 年間の冷房負荷 [MWh/年]
anual_cooling_load = np.sum( data["ZONE1:Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000000
print(f"年間冷房負荷 MWh {anual_cooling_load}")

# 最大暖房負荷 [kW]
maximum_heating_load = np.max( data["ZONE1:Zone Air System Sensible Heating Energy [J](Hourly)"] ) /3600 /1000
print(f"最大暖房負荷 kW {anual_heating_load}")

# 最大冷房負荷 [kW]
maximum_cooling_load = np.max( data["ZONE1:Zone Air System Sensible Cooling Energy [J](Hourly) "] ) /3600 /1000
print(f"最大冷房負荷 kW {maximum_cooling_load}")

# 年間積算日射量（全天） [kWh/m2]
solar_radiation_N = np.sum( data["WALL_N:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_E = np.sum( data["WALL_E:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_W = np.sum( data["WALL_W:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_S = np.sum( data["WALL_S:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000
solar_radiation_H = np.sum( data["ROOF:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]) /1000

print(f"年間積算日射量（全天）北 kWh/m2 {solar_radiation_N}")
print(f"年間積算日射量（全天）東 kWh/m2 {solar_radiation_E}")
print(f"年間積算日射量（全天）西 kWh/m2 {solar_radiation_W}")
print(f"年間積算日射量（全天）南 kWh/m2 {solar_radiation_S}")
print(f"年間積算日射量（全天）水平 kWh/m2 {solar_radiation_H}")

# 曇天日3/5の南面・西面日射量 [Wh/m2]
print("--- 3/5 南面 ---")
print(data["WALL_S:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"])
print("--- 3/5 西面 ---")
print(data["WALL_W:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"])

# 晴天日7/27の南面・西面日射量 [Wh/m2]
print("--- 7/27 南面 ---")
print(data["WALL_S:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"])
print("--- 7/27 西面 ---")
print(data["WALL_W:Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"])

# 代表日1/4の冷暖房負荷（Case 600）
hourly_heatload_winter = ( data["ZONE1:Zone Air System Sensible Heating Energy [J](Hourly)"]["2021/1/4"] - \
    data["ZONE1:Zone Air System Sensible Cooling Energy [J](Hourly) "]["2021/1/4"] ) /3600 /1000

print("--- 1/4 冷暖房負荷 ---")
print(hourly_heatload_winter)


# %%
