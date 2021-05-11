#%%
import pandas as pd
import numpy as np

# ケース名の入力
CASENAME = "Case900_J1_2"

file_list = {

    "Case600": {
        "memo": "宮田作成ファイル Case600",
        "case_ID" : "600",
        "filename": "./idf_miyata/case600.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case610": {
        "memo": "宮田作成ファイル Case610",
        "case_ID" : "610",
        "filename": "./idf_miyata/case610.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case620": {
        "memo": "宮田作成ファイル Case620",
        "case_ID" : "620",
        "filename": "./idf_miyata/case620.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_E1",
            "window_name_2" : "WINDOW_W1"
        }
    },

    "Case630": {
        "memo": "宮田作成ファイル Case630",
        "case_ID" : "630",
        "filename": "./idf_miyata/case630.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_E1",
            "window_name_2" : "WINDOW_W1"
        }
    },

    "Case640": {
        "memo": "宮田作成ファイル Case640",
        "case_ID" : "640",
        "filename": "./idf_miyata/case640.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case650": {
        "memo": "宮田作成ファイル Case650",
        "case_ID" : "650",
        "filename": "./idf_miyata/case650_v2.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case650FF": {
        "memo": "宮田作成ファイル Case650FF",
        "case_ID" : "650FF",
        "filename": "./idf_miyata/case650FF.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case900": {
        "memo": "宮田作成ファイル Case900",
        "case_ID" : "900",
        "filename": "./idf_miyata/case900.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case900FF": {
        "memo": "宮田作成ファイル Case900FF",
        "case_ID" : "900FF",
        "filename": "./idf_miyata/case900FF.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case900_J1_1": {
        "memo": "宮田作成ファイル Case900_J1_1",
        "case_ID" : "Case900_J1_1",
        "filename": "./idf_miyata/case900_J1_1.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case900_J1_2": {
        "memo": "宮田作成ファイル Case900_J1_2",
        "case_ID" : "Case900_J1_2",
        "filename": "./idf_miyata/case900_J1_2.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case910": {
        "memo": "宮田作成ファイル Case910",
        "case_ID" : "910",
        "filename": "./idf_miyata/case910.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case920": {
        "memo": "宮田作成ファイル Case920",
        "case_ID" : "920",
        "filename": "./idf_miyata/case920.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_E1",
            "window_name_2" : "WINDOW_W1"
        }
    },

    "Case930": {
        "memo": "宮田作成ファイル Case930",
        "case_ID" : "930",
        "filename": "./idf_miyata/case930.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_E1",
            "window_name_2" : "WINDOW_W1"
        }
    },

    "Case940": {
        "memo": "宮田作成ファイル Case940",
        "case_ID" : "640",
        "filename": "./idf_miyata/case940.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case950": {
        "memo": "宮田作成ファイル Case950",
        "case_ID" : "950",
        "filename": "./idf_miyata/case950.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case950FF": {
        "memo": "宮田作成ファイル Case950FF",
        "case_ID" : "950FF",
        "filename": "./idf_miyata/case950FF.csv",
        "name_dict" : {
            "zone_name"   : "ZONE1",
            "wall_name_s" : "WALL_S",
            "wall_name_n" : "WALL_N",
            "wall_name_w" : "WALL_W",
            "wall_name_e" : "WALL_E",
            "roof_name"   : "ROOF",
            "window_name_1" : "WINDOW_S1",
            "window_name_2" : "WINDOW_S2"
        }
    },

    "Case600_AS140": {
        "memo": "AS140公式ファイル Case600",
        "case_ID" : "600",
        "filename": "./idf_miyata/Case600_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1",
            "window_name_2" : "ZONE SUBSURFACE 2"
        }
    },

    "Case620_AS140": {
        "memo": "AS140公式ファイル Case620",
        "case_ID" : "620",
        "filename": "./idf_miyata/Case620_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1 EAST WINDOW",
            "window_name_2" : "ZONE SUBSURFACE 2 WEST WINDOW"
        }
    },

    "Case630_AS140": {
        "memo": "AS140公式ファイル Case630",
        "case_ID" : "630",
        "filename": "./idf_miyata/Case630_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1 EAST WINDOW",
            "window_name_2" : "ZONE SUBSURFACE 2 WEST WINDOW"
        }
    },

    "Case640_AS140": {
        "memo": "AS140公式ファイル Case640",
        "case_ID" : "640",
        "filename": "./idf_miyata/Case640_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1",
            "window_name_2" : "ZONE SUBSURFACE 2"
        }
    },

    "Case650_AS140": {
        "memo": "AS140公式ファイル Case650",
        "case_ID" : "650",
        "filename": "./idf_miyata/Case650_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1",
            "window_name_2" : "ZONE SUBSURFACE 2"
        }
    },
    
    "Case650FF_AS140": {
        "memo": "AS140公式ファイル Case650FF",
        "case_ID" : "650FF",
        "filename": "./idf_miyata/Case650FF_AS140.csv",
        "name_dict" : {
            "zone_name"   : "ZONE ONE",
            "wall_name_s" : "ZONE SURFACE SOUTH",
            "wall_name_n" : "ZONE SURFACE NORTH",
            "wall_name_w" : "ZONE SURFACE WEST",
            "wall_name_e" : "ZONE SURFACE EAST",
            "roof_name"   : "ZONE SURFACE ROOF",
            "window_name_1" : "ZONE SUBSURFACE 1",
            "window_name_2" : "ZONE SUBSURFACE 2"
        }
    },

    "Case600_Ono": {
        "memo": "小野さん作成ファイル Case600",
        "case_ID" : "600",
        "filename": "./idf_miyata/case600_ono.csv",
        "name_dict" : {
            "zone_name"   : "BLOCK1:ZONE1",
            "wall_name_s" : "BLOCK1:ZONE1_WALL_S",
            "wall_name_n" : "BLOCK1:ZONE1_WALL_N",
            "wall_name_w" : "BLOCK1:ZONE1_WALL_W",
            "wall_name_e" : "BLOCK1:ZONE1_WALL_E",
            "roof_name"   : "BLOCK1:ZONE1_ROOF_1_0_0"
        }
    },

}


filename =  file_list[CASENAME]["filename"]
name_dict = file_list[CASENAME]["name_dict"]

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

df_results[CASENAME] = pd.Series({

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
df_results[CASENAME]["transmissivity_coefficient"] = df_results[CASENAME]["solar_transitted"] / df_results[CASENAME]["solar_radiation_S"]

# 曇天日3/5の南面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_March_5_south_"+str(hh)] = data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"][hh]
df[CASENAME] = pd.Series(tmp)
df_results = df_results.append(df)

# 曇天日3/5の西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_March_5_west_"+str(hh)] = data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/3/5"][hh]
df[CASENAME] = pd.Series(tmp)
df_results = df_results.append(df)

# 晴天日7/27の南面・西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_July_27_south_"+str(hh)] = data[ name_dict["wall_name_s"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"][hh]
df[CASENAME] = pd.Series(tmp)
df_results = df_results.append(df)

# 曇天日7/27の西面日射量 [Wh/m2]
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["solar_radiation_July_27_west_"+str(hh)] = data[ name_dict["wall_name_w"] + ":Surface Outside Face Incident Solar Radiation Rate per Area [W/m2](Hourly)"]["2021/7/27"][hh]
df[CASENAME] = pd.Series(tmp)
df_results = df_results.append(df)


# 代表日1/4の冷暖房負荷
df = pd.DataFrame()
tmp = {}
for hh in range(0,24):
    tmp["hourly_heatload_winter_"+str(hh)] = ( data[ name_dict["zone_name"] + ":Zone Air System Sensible Heating Energy [J](Hourly)"]["2021/1/4"][hh] - \
        data[ name_dict["zone_name"] + ":Zone Air System Sensible Cooling Energy [J](Hourly) "]["2021/1/4"][hh] ) /3600 /1000
df[CASENAME] = pd.Series(tmp)
df_results = df_results.append(df)


#--------------------------------
# for Case 620
#--------------------------------

if file_list[CASENAME]["case_ID"] == "620" or file_list[CASENAME]["case_ID"] == "630":

    # 年間積算透過日射量（全天、庇なし） 西面
    df = pd.DataFrame()
    df[CASENAME] = pd.Series({
        "solar_transitted_West"  : np.sum( data[ name_dict["window_name_2"] + ":Surface Window Transmitted Solar Radiation Rate [W](Hourly)"]) /1000 /6,   # 窓面透過日射量 [kWh/m2]
        })
    df_results = df_results.append(df)


#--------------------------------
# for Case 600FF, 900FF etc 自然室温ケース
#--------------------------------

if "FF" in file_list[CASENAME]["case_ID"]:

    # 自然室温の最大・最小・平均
    df = pd.DataFrame()
    tmp = {}
    tmp["maximum_free_float_temperature"] = np.max( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
    tmp["minimum_free_float_temperature"] = np.min( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
    tmp["average_free_float_temperature"] = np.mean( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"] )
    df[CASENAME] = pd.Series(tmp)
    df_results = df_results.append(df)

    # 代表日1/4と7/27の自然室温
    df = pd.DataFrame()
    tmp = {}
    for hh in range(0,24):
        tmp["free_float_temperature_Jan04_"+str(hh)] = ( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021/1/4"][hh] )
    for hh in range(0,24):
        tmp["free_float_temperature_Jul27_"+str(hh)] = ( data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"]["2021/7/27"][hh] )
    df[CASENAME] = pd.Series(tmp)
    df_results = df_results.append(df)


# 室温の頻度分布
if file_list[CASENAME]["case_ID"] == "900FF":

    # 室温の範囲
    temperature_range = np.arange(-50,99)
    # 結果格納用変数
    temperature_distribution = np.zeros(len(temperature_range))

    for templerature in data[ name_dict["zone_name"] + ":Zone Mean Air Temperature [C](Hourly)"]:
        
        for i in range(len(temperature_range)):
            if temperature_range[i] > templerature:
                temperature_distribution[i] += 1
                break

    # 追加
    df = pd.DataFrame()
    tmp = {}
    for i in range(len(temperature_range)):
        tmp["room_air_temperature_distribution_"+str(temperature_range[i])] = ( temperature_distribution[i] )
    df[CASENAME] = pd.Series(tmp)
    df_results = df_results.append(df)


df_results.to_csv("集計結果_"+ CASENAME + ".csv")




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
