#%%
import pandas as pd

filename = "./results/case600/case600.csv"

#%%

# 時刻ラベルを生成
dates = pd.date_range(start='1/1/2021 0:00:00', end='12/31/2021 23:00:00', freq='H')

# データの読み込み
data  = pd.read_csv(filepath_or_buffer=filename, sep=",", header=[0], encoding="cp932")

# インデックスの設定
data.index = dates
data.index.name = "data_hour"

# 確認
print(data["WALL_S:Surface Outside Face Sunlit Area [m2](Hourly)"]["2021-01-01 7:00:00":"2021-01-01 17:00:00"])

# %%
