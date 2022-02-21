class Config(object):
    '''
    A config class to regulate all the variables in the system
    '''
    def __init__(self) -> None:
        self.vessel_interval_scale=200
        self.vessel_containers=5000
        self.train_speed=8
        self.train_capacity=200
        self.train_interval_scale=8
        self.truck_capacity=1
        self.offloader_speed=25
        self.loader_speed=25
        self.truck_speed=3
