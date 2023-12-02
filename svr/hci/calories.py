import pandas as pd
MET = 3.5
WEIGHT = 60
# 1MET = 휴식 또는 안정 시 에너지 소비량
# 성인 기준 산소 소비량 3.5ml/kg/min
# (MET * 3.5 * 0.001 * 체중) * 5 : 분당 칼로리 소모량

# calories_group1 = []
# calories_group2 = []
# calories_group3 = []
#
# # 강도 1
# # 5.625km/h 100m 64초
# # 3.5MET
# calories1 = (((3.5 * MET) * 0.001 * WEIGHT) * 5) / 20
# start = 0
# for i in range(20 * 60):
#     calories_group1.append(start)
#     start = start + calories1
#
# # 강도 2
# # 8.0km/h
# # 7MET
# calories2 = (((7 * MET) * 0.001 * WEIGHT) * 5) / 20
# start = 0
# for i in range(20 * 60):
#     calories_group2.append(start)
#     start = start + calories2
#
# # 강도 3
# # 12km/h
# # 12MET
# calories3 = (((12 * MET) * 0.001 * WEIGHT) * 5) / 20
# start = 0
# for i in range(20 * 60):
#     calories_group3.append(start)
#     start = start + calories3
#
# print(calories_group1)
# print(calories_group2)
# print(calories_group3)


def get_calories(strength, weight):
    calories_list = []

    if strength == 1:
        num = 3.5
    elif strength == 2:
        num = 7
    else:
        num = 12

    start = 0
    for i in range(20 * 60):
        calories_list.append(start)
        start = start + (((num * MET) * 0.001 * weight) * 5) / 20

    return calories_list

# print(get_calories(1, 60))