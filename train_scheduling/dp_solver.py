import math
from train_scheduling.train_model import TrainSchedule

class DPSolver:
    def __init__(self, schedule, config):
        self.schedule = schedule
        self.config = config
        self.dp_table = {}

    def solve(self):
        for train in self.schedule.non_fixing_trains:
            self.dp_table[train.train_id] = {}
        for train in self.schedule.non_fixing_trains:
            self._dp_step(train)
        self._retrieve_solution()

    def _dp_step(self, train):
        print(f"Processing train {train.train_id} in DP step")

    def _retrieve_solution(self):
        print("Retrieving solution...")
        self.schedule.display_schedule()

    def calculate_service(self, train_a, train_b):
        slack_time = train_b.departure_time - train_a.arrival_time - self.config['transfer_time']
        return math.exp(-slack_time)