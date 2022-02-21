from Components import Vessel, Offloader, Truck, Loader, Train, Map, Counter
from Action import Actions
from logger import logger as logging
from SeaportGenerator import SeaportGenerator
from utils import cal_delta2, cal_delta3, cal_average_truck_time,get_random
from tqdm import trange
from Config import Config

config=Config()

SeaportGenerator = SeaportGenerator(100, 100, 0.0003, 0.3)
matrix = SeaportGenerator.get_random_network()
matrix = matrix/10
head_to_list = SeaportGenerator.get_head_to_list(matrix)


Offloader = Offloader(speed=config.offloader_speed, container=0)
Loader = Loader(speed=config.loader_speed, container=0)
Map = Map(head_to_list, matrix)
Counter = Counter(len(matrix)-1)


Actions = Actions()

truck_n = 0
train_n = 0
truck_list = []
truck_arrive_list = []
interval_time_vessel=0
interval_time_train=0
offload_time=0

for world_time in trange(2400):
    interval_time_vessel+=1
    interval_time_train+=1
    if Actions.Vessel_Come(scale=config.vessel_interval_scale, time=interval_time_vessel):
        vessel=Vessel(container=config.vessel_containers)
        offload_time += Actions.Vessel_Offload_Times(Vessel=vessel, Offloader=Offloader)
        interval_time_vessel=0

    if Actions.Train_Come(time=interval_time_train, scale=config.train_interval_scale):
        train = Train(speed=config.train_speed, container=0, capacity=config.train_capacity, status=True)
        train.info["number"] = train_n
        train.info["start_time"] = world_time
        train_n += 1
        Counter.train_stay.append(train)
        interval_time_train=0

    if offload_time > 0:
        Actions.Offloader_Containers(Offloader=Offloader)
        truck_num = Actions.Truck_Get_Containers(Offloader=Offloader)
        for i in range(truck_num):
            truck = Truck(speed=config.truck_speed,active=True,capacity=config.truck_capacity)
            truck.info["start_time"] = world_time
            truck.info["number"] = truck_n
            truck_n += 1
            Counter.truck_num_list[0] += 1
            truck_list.append(truck)

    for truck in truck_list:
        #logging.debug("truck:"+str(truck.info)+"headto:"+str(truck.head_to))
        if truck.active:
            Actions.Truck_Go(Truck=truck, Map=Map, Loader=Loader, time=0.03, Counter=Counter)
            truck.info["active_time"] += 1
            if not truck.active:
                truck_list.remove(truck)
                truck_arrive_list.append(truck)
        else:
            truck_list.remove(truck)
            truck_arrive_list.append(truck)

    if len(Counter.train_stay) > 0 and Loader.container > 0:
        logging.debug("Loader Container Num:"+str(Loader.container))
        Actions.Load_to_Train(
            Loader=Loader, Train=Counter.train_stay[0], time=world_time, Counter=Counter)

    for train in Counter.train_go:
        logging.debug("Train:"+str(train.info))

    offload_time -= 1
    logging.debug("-------------time: "+str(world_time)+"---------------")


# print(Counter.train_go[0].info["last_cargo"])

delta1 = 1-float(Offloader.speed)*100/15/348
delta1 = 0.8*delta1
logging.info("Delta1: "+str(delta1))

delta2 = cal_delta2(Counter.train_go)
logging.info("Delta2: "+str(delta2))

delta3,(v_star, v_sigma, v_average) = cal_delta3(Counter.train_go)
logging.info("Delta3: "+str(delta3))
logging.info("v_star: "+str(v_star))
logging.info("v_sigma: "+str(v_sigma))
logging.info("v_average: "+str(v_average))

m = 1/(1+delta1/3+delta2/3+delta3/3)
logging.info("M: "+str(m))

truck_average_transfer_time = cal_average_truck_time(truck_arrive_list)
logging.info("Truck_Average_Time: "+str(truck_average_transfer_time))


logging.info("Train Departure Num: "+str(len(Counter.train_go)))
logging.info("Truck Arrived Num: "+str(len(truck_arrive_list)))
logging.info("Loader Container Num: "+str(Loader.container))
logging.info("First Train Container: "+str(Counter.train_stay[0].container))
