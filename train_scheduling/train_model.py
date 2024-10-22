class Train:
    def __init__(self, train_id, arrival_time=None, departure_time=None, is_fixing=False):
        self.train_id = train_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.is_fixing = is_fixing
        self.connected_trains = []

    def set_schedule(self, arrival_time, departure_time):
        self.arrival_time = arrival_time
        self.departure_time = departure_time

    def add_connection(self, other_train):
        self.connected_trains.append(other_train)

class TrainSchedule:
    def __init__(self):
        self.fixing_trains = []
        self.non_fixing_trains = []

    def add_train(self, train):
        if train.is_fixing:
            self.fixing_trains.append(train)
        else:
            self.non_fixing_trains.append(train)

    def get_train(self, train_id):
        all_trains = self.fixing_trains + self.non_fixing_trains
        return next(train for train in all_trains if train.train_id == train_id)

    def display_schedule(self):
        for train in self.fixing_trains + self.non_fixing_trains:
            print(f"Train {train.train_id}: Arrival = {train.arrival_time}, Departure = {train.departure_time}")