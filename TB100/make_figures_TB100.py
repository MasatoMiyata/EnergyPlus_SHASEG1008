#%%
%matplotlib widget

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

# グラフ文字化け対策
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams["font.size"] = 18


#%%
# データの読み込み

# 時刻ヘッダー
dates = pd.date_range(start='1/1/2021 1:00:00', end='1/1/2022 0:00:00', freq='H')

def import_data(filename):
    """
    結果が格納されたExcelファイルを読み込む関数
    """
    data = pd.read_excel(filename, sheet_name="TB100_年間データ", index_col=0, header=0)
    data.index = dates
    data.index.name = "date_hour"
    return data

df_BEST = import_data("熱負荷テスト(建物全体テスト)_年間出力データフォーマット案_TB100_BEST.xlsx")
df_newHASP = import_data("熱負荷テスト(建物全体テスト)_年間出力データフォーマット案_TB100_NewHASP.xlsx")
df_EnergyPlus = import_data("熱負荷テスト(建物全体テスト)_年間出力データフォーマット案_TB100_EnergyPlus.xlsx")

#%%

room_list = [
    "1F廊下",
    "1Fロビー",
    "1FEVホール",
    "1F中央監視室",
    "1F更衣室1",
    "1F更衣室2",
    "1F休憩室",
    "1F自販機ｺｰﾅｰ",
    "1F事務室1",
    "1F事務室2",
    "2-6F廊下",
    "2-6F自販機ｺｰﾅｰ",
    "2-6FEVホール",
    "2-6F事務室1NP",
    "2-6F事務室1NEP",
    "2-6F事務室1NWP",
    "2-6F事務室1NI",
    "2-6F事務室2SP",
    "2-6F事務室2SWP",
    "2-6F事務室2SI",
    "7F廊下",
    "7F自販機ｺｰﾅｰ",
    "7FEVホール",
    "7F事務室1",
    "7F事務室2",
]

item_list = [
    "顕熱",
    "潜熱",
    "温度",
    "湿度"
]

#%%

def make_figure(item, room):
    """
    グラフを作成する関数
    """

    # 列名    
    item_name = item + "(" + room + ")"

    fig = plt.figure(figsize=(10,7))
    # plt.subplots_adjust(left=0.09, bottom=0.05, right=0.97, top=0.95, wspace=0.15, hspace=0.40)

    ax = fig.add_subplot(1,1,1)
    ax.plot(df_BEST[ item_name ], 'r', linewidth=0.7, label="BEST") 
    ax.plot(df_newHASP[ item_name ], 'g', linewidth=0.7, label="newHASP") 
    ax.plot(df_EnergyPlus[ item_name ], 'b', linewidth=0.7, label="EnergyPlus") 
    ax.legend()
    ax.grid()
    ax.set_title( room + ": " + item)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

    if item == "室温":
        ax.set_ylabel("室温 [℃]")
        ax.set_ylim([5,35])
    elif item == "湿度":
        ax.set_ylabel("湿度 [kg/kgDA]")
        ax.set_ylim([0,0.02])


make_figure("温度", "7F事務室1")
make_figure("湿度", "7F事務室1")
make_figure("顕熱", "7F事務室1")
make_figure("潜熱", "7F事務室1")



# %%
