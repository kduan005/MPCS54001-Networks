import time

# https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
# current_milli_time function return the current time in milliseconds' format
current_milli_time = lambda: int(round(time.time() * 1000))
