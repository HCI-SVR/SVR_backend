import pandas as pd
import pymysql
from svr.models import Music
from svr import db
import requests

df = pd.read_csv('../resources/spotify_data.csv')

# print(df)
# print(df.columns)
# print(df['tempo'])
# print(df['tempo'].describe())
# print(df[df["tempo"] > 200])

bins = [0, 120, 140, 160, 180, float('inf')]
df['group'] = pd.cut(df['tempo'], bins=bins, labels=[1, 2, 3, 4, 5])

# 각 그룹의 개수 출력
group_counts = df['group'].value_counts()
print(group_counts)

nan_rows = df[df.isnull().any(axis=1)]
print(nan_rows)
df = df.dropna()

print(df.columns)

# for i in range(len(df)):
#     song = df.iloc[i]
#     # print(type(song.group))
#     data = {
#         "name": song.track,
#         "singer": song.artist,
#         "group_id": int(song.group),
#         "uri": song.uri,
#         "image_key": song.image_url,
#     }
#
#     # music = Music(name=name, singer=singer, group_id=group_id,
#     #               uri=uri, image_key=image_key)
#     # db.session.add(music)
#     # db.session.commit()
#     url = "http://127.0.0.1:5000/music/insert"
#     response = requests.post(url, json=data)
#     if response.status_code == 200:
#         print("post 성공")
#     else:
#         print("post 실패")
#         print("상태 코드: ", response.status_code, response.text)
#
