# # 5초에 한번씩 update 예정
# distance_group1 = []
# distance_group2 = []
# distance_group3 = []
#
# # 강도 1 (빠르게 걷기)
# # 5.625km/h 100m 64초
# # 5초에 0.00781km
# start = 0
# for i in range(20 * 60):
#     distance_group1.append(start)
#     start = start + 0.00781
#
# # 강도 2 (조깅)
# # 8km/h, 100m 45초
# # 5초에 0.0111km
# start = 0
# for i in range(20 * 60):
#     distance_group2.append(start)
#     start = start + 0.0111
#
# # 강도 3 (러닝)
# # 12km/h 100m 30초
# # 5초에 0.01665m
# start = 0
# for i in range(20 * 60):
#     distance_group3.append(start)
#     start = start + 0.01665
#
# print(distance_group1)
# print(distance_group2)
# print(distance_group3)


def get_distance(group_id):
    if group_id == 1:
        velocity = 0.00781
    elif group_id == 2:
        velocity = 0.0111
    else:
        velocity = 0.01665

    distance_list = []
    start = 0
    for i in range(20 * 60):
        distance_list.append(start)
        start = start + velocity
    return distance_list
