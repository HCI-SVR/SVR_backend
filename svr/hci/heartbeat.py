import numpy as np
import matplotlib.pyplot as plt

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
        start = 0
        end = 0.5    # 120
        max_heartbeat *= 0.6
    elif group_id == 2:
        start = 0
        end = 0.6875    #150
        max_heartbeat *= 0.75
    else:
        start = 0
        end = 0.75    #160
        max_heartbeat *= 0.8

    current_heartbeat = 60  # 초기 심박수
    heartbeat_list.append(current_heartbeat)
    count = 0
    for i in range(20 * 60):
        # 랜덤한 값으로 심박수를 조금씩 증가시킴

        if i > 1000:
            if np.random.rand() < 0.6 and current_heartbeat > 60:  # 10%의 확률로 감소하며 최소 심박수가 60임
                decrement = np.random.uniform(0, 0.5)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat -= decrement
            else:
                increment = np.random.uniform(0, 0.5)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat += increment
            heartbeat_list.append(current_heartbeat)

        elif 400 <= i <= 1000:
            if np.random.rand() < 0.5 and current_heartbeat > 60:  # 10%의 확률로 감소하며 최소 심박수가 60임
                decrement = np.random.uniform(0, 0.5)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat -= decrement
            else:
                increment = np.random.uniform(0, 0.5)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat += increment
            heartbeat_list.append(current_heartbeat)

        else:
            # 일정 확률로 심박수를 감소시킴
            if np.random.rand() < 0.2 and current_heartbeat > 60:  # 10%의 확률로 감소하며 최소 심박수가 60임
                decrement = np.random.uniform(0, 0.5)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat -= decrement
            else:
                increment = np.random.uniform(start, end)  # 필요에 따라 범위를 조절할 수 있습니다.
                current_heartbeat += increment
            heartbeat_list.append(current_heartbeat)

        # 심박수가 지정된 범위 내에 있도록 보장
        # heartbeat_list.append(np.random.randint(round(max_heartbeat * start), round(max_heartbeat * end)))

        if current_heartbeat > max_heartbeat:
            count += 1
    # increment_per_sample = (180 - 60) / (20 * 60)
    # heartbeat_list = [60 + i * increment_per_sample for i in range(20 * 60)]
    return heartbeat_list


# heartbeat = get_heartbeat(3, 20)
# plt.plot(heartbeat)
# plt.xlabel('Time')
# plt.ylabel('Heartbeat')
# plt.title('Heartbeat Pattern')
# plt.show()
# print(heartbeat)
print(get_heartbeat(3, 20))


