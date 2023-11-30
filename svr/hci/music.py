import pandas as pd

df = pd.read_csv('../resources/track_and_features.csv')

print(df)
print(df.columns)
print(df['tempo'])
print(df['tempo'].describe())
print(df[df["tempo"] > 200])

bins = [0, 120, 140, 160, 180, float('inf')]
df['group'] = pd.cut(df['tempo'], bins=bins, labels=['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'])

# 각 그룹의 개수 출력
group_counts = df['group'].value_counts()
print(group_counts)
