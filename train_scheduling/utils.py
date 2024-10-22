def calculate_time_window(arrival, departure, min_time, max_time):
    return range(max(arrival + min_time, 0), min(departure + max_time, 24))

def validate_constraints(train, config):
    return config['min_dwell_time'] <= train.departure_time - train.arrival_time <= config['max_dwell_time']