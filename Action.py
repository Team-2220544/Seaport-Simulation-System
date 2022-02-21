import random
from Config import Config
from utils import get_random

random.seed(1)
config = Config()


class Actions():
    def __init__(self):
        pass

    def Vessel_Come(self, scale, time):
        """
        Tell whether a ship has arrive
        scale: 1/lambda of possion process
        time: the time interval since last ship arrive
        """
        if time > get_random(scale) or time == 0:
            return True
        else:
            return False

    def Vessel_Offload_Times(self, Vessel, Offloader):
        """
        Calculate the time need to offload all the containers from ship to barth
        """
        time_cost = Vessel.container/Offloader.speed
        return time_cost

    def Offloader_Containers(self, Offloader):
        '''
        Offload containers from ship to barth
        '''
        Offloader.container += Offloader.speed

    def Truck_Get_Containers(self, Offloader):
        if Offloader.container:
            truck_num = Offloader.container//config.truck_capacity
            Offloader.container = 0
            return truck_num

    def Truck_Go(self, Truck, Map, Loader, time, Counter):
        if not Truck.active:
            return
        Truck.rest_way -= time*Truck.speed
        if Truck.rest_way <= 0:
            if Truck.head_to == Map.terminal:
                Loader.container += 1
                Truck.active = False
                Counter.truck_num_list[Truck.head_to] -= 1
                return
            Counter.truck_num_list[Truck.head_to] -= 1
            truck_current = Truck.head_to
            next_head = Map.node_link_list[Truck.head_to]
            next_option = Map.node_link_list[truck_current]
            Truck.head_to = next_option[random.randint(0, len(next_head)-1)]
            Counter.truck_num_list[Truck.head_to] += 1
            Truck.rest_way = Map.matrix[truck_current][Truck.head_to]

    def Train_Come(self, time, scale):
        """
        Tell whether a train has arrive
        prama: scale: 1/lambda of possion process
        prama: time: the time interval since last train arrive
        """
        if time > get_random(scale):
            return True
        else:
            return False

    def Load_to_Train(self, Loader, Train, time, Counter):
        if Train.container == 0 and Loader.container:
            Train.info["first_cargo"] = time

        if Loader.container >= Train.capacity-Train.container and Train.info["last_cargo"] == 0:
            Train.info["last_cargo"] = time

        if Train.container+min(Loader.container, Loader.speed) >= Train.capacity:
            Train.status = False
            Train.info["leave_time"] = time
            Counter.train_go.append(Counter.train_stay.pop(0))
            Loader.container -= Train.capacity-Train.container
        else:
            Train.container += min(Loader.container, Loader.speed)
            Loader.container -= min(Loader.container, Loader.speed)
