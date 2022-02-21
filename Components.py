class Vessel():
    def __init__(self, container):
        '''
        prarm: speed: Vessel's speed to enter port
        prarm: container: Container num a vessel hold
        '''
        self.container = container


class Offloader():
    def __init__(self, speed, container=0):
        '''
        prarm: speed: Offloader's speed to offload
        prarm: container: Current container number of the port
        '''
        self.speed = speed
        self.container = container


class Truck():
    def __init__(self, speed, rest_way=0, head_to=0, capacity=1, active=False):
        '''

        '''
        self.speed = speed
        self.rest_way = rest_way
        self.head_to = head_to
        self.active = active
        self.capacity=capacity
        self.info = {"number": 0, "start_time": 0, "active_time": 0}


class Loader():
    def __init__(self, speed, container):
        self.speed = speed
        self.container = container


class Train():
    def __init__(self, speed, container, capacity, status=False):
        self.speed = speed
        self.container = container
        self.capacity = capacity
        self.status = False
        self.flag = 1
        self.info = {"number": 0, "start_time": 0,
                     "leave_time": 0, "first_cargo": 0, "last_cargo": 0}


class Map():
    def __init__(self, node_link_list, matrix):
        self.node_link_list = node_link_list
        self.terminal = len(node_link_list)-1
        self.matrix = matrix


class Counter():
    def __init__(self, terminal):
        self.truck_num_list = [0]*(terminal+1)
        self.train_go = []
        self.train_stay = []
