import shutil

src = './data/data_today.csv'
dst = './data/data_today_wrong.csv'
shutil.copyfile(src, dst)