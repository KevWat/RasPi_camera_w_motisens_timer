import time
import threading

    
def scheduler(interval, fnc, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = fnc) # set fnc as execute method
        t.start()
        if wait:
            t.join() # Block call next thread until current thread
        # Excute time - Currrent time
        next_time = ((base_time - time.time()) % interval ) or interval
        time.sleep(next_time)

# example
'''
def worker():
    print(time.time())
    time.sleep(8)

scheduler(1*60, worker, False) # unit:sec, False: Paralell, Ture: Single
'''
