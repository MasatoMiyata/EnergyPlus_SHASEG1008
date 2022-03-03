import os

path = "./01_Load_Test/02_Building"

# ファイル名の取得
files = os.listdir(path)
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

# 不要なファイルの削除
for filename in files_file:

    for extension in [".audit", ".bnd", "dxf", "eio", "err", "eso", "mtd", "rvaudit", "shd", "svg", "mtr", "Zsz.csv", "mtr", ".rdd", ".mdd" ]:
    
        if filename.endswith(extension):
            os.remove(path + "/" + filename)