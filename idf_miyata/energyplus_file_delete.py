import os

path = "./idf_miyata"

# ファイル名の取得
files = os.listdir(path)
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

# ファイルの削除
for filename in files_file:

    for extension in [".audit", ".bnd", "dxf", "eio", "err", "eso", "mdd", "mtd", "rdd", "rvaudit", "shd", "svg"]:
    
        if filename.endswith(extension):
            os.remove(path + "/" + filename)