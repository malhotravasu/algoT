""" Commonly used functions """

def get_closest_stamp(index, timestamp, delta, type='start'):
    if type == 'start':
        closest = timestamp
        while closest not in index:
            closest += delta
        return closest
    elif type == 'end':
        closest = timestamp
        while closest not in index:
            closest -= delta
        return closest