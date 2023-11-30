import numpy as np

# heartbeat_group1 = []
# heartbeat_group2 = []
# heartbeat_group3 = []
#
#
# # 220 - 20(20이라고 가정)
# max_heartbeat = 200
#
# # 강도 1
# # 가벼운 운동 50 ~ 60%
# for i in range(20 * 60):
#     heartbeat_group1.append(np.random.randint(200 * 0.5, round(200 * 0.6)))
#
# # 강도 2
# # 다이어트 60 ~ 75%
# for i in range(20 * 60):
#     heartbeat_group2.append(np.random.randint(round(200 * 0.6), round(200 * 0.75)))
#
# # 강도 3
# # 지구력과 근지구력 75 ~ 80%
# for i in range(20 * 60):
#     heartbeat_group3.append(np.random.randint(round(200 * 0.75), round(200 * 0.8)))
#
#
# print(heartbeat_group1)
# print(heartbeat_group2)
# print(heartbeat_group3)


def get_heartbeat(group_id, age):

    heartbeat_list = []
    max_heartbeat = 220 - age
    if group_id == 1:
        start = 0.5
        end = 0.6
    elif group_id == 2:
        start = 0.6
        end = 0.75
    else:
        start = 0.75
        end = 0.8

    for i in range(20 * 60):
        heartbeat_list.append(np.random.randint(round(max_heartbeat * start), round(max_heartbeat * end)))
    return heartbeat_list
