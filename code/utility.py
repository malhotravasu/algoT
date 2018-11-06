""" Commonly used functions """

def get_next_stamp(index, timestamp, delta):
    closest = timestamp
    while closest not in index:
        closest += delta
    return closest