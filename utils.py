
def cal_delta2(train_list):
    """
    function to calculate delta2
    param: train_list: a train list contain trains and each train has its info
    """
    delta_sum = 0
    for train in train_list:
        cnarr = float(train.info["last_cargo"])/100
        c1arr = float(train.info["first_cargo"])/100
        tarr = float(train.info["start_time"])/100
        delta = (max(cnarr-tarr, 0)/(200*(cnarr-c1arr+0.1)))
        delta_sum += delta
    delta2 = delta_sum/len(train_list)
    return delta2


def cal_delta3(train_list):
    """
    function to calculate delta3
    param: train_list: a train list contain trains and each train has its info
    """
    v_list = []
    for train in train_list:
        cnarr = float(train.info["last_cargo"])/100
        c1arr = float(train.info["first_cargo"])/100
        tarr = float(train.info["start_time"])/100
        tdep = float(train.info["leave_time"])/100
        alpha = (tdep-max(c1arr, tarr))/(tdep-tarr+0.1)
        vshift = alpha*(tdep-cnarr+0.1)
        v_list.append(vshift)
    v_average = sum(v_list)/len(v_list)
    v_sigma = [(v-v_average)**2 for v in v_list]
    v_sigma = sum(v_sigma)/len(train_list)**0.5
    v_star = max(v_list)
    delta3 = 0.2*v_sigma/v_average+0.8*(v_star-v_average)/v_star
    return delta3, (v_star, v_sigma, v_average)


def cal_average_truck_time(truck_list):
    """
    function to calculate the average time a truck use on the transfering way
    param: truck_list: a truck list contain trucks and each truck has its info
    """
    truck_average_transfer_time = 0
    for truck in truck_list:
        truck_average_transfer_time += truck.info["active_time"]
    truck_average_transfer_time /= len(truck_list)
    return truck_average_transfer_time


def get_random(scale, size=[1, 1]):
    """
    fuction to random a possion process number
    param: scale: 1/lambda
    param: size: output vector size
    """
    from numpy import random
    return random.exponential(scale=scale, size=size)[0][0]
