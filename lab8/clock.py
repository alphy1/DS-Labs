from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def calc_recv_timestamp(recv_time_stamp, counter):
    for i in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i])
    
    return counter

def event(pid, counter):
    counter[pid] += 1
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    return counter

def recieve_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter[pid] += 1
    counter = calc_recv_timestamp(timestamp, counter)
    return counter

def process1(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recieve_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recieve_message(pipe12, pid, counter)
    print('Process 1: ', counter)

def process2(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = recieve_message(pipe21, pid, counter)
    counter = recieve_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recieve_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)
    print('Process 2: ', counter)

def process3(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = send_message(pipe32, pid, counter)
    counter = recieve_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recieve_message(pipe32, pid, counter)
    print('Process 3: ', counter)

if __name__ == '__main__':    
    pipe12, pipe21 = Pipe()
    pipe23, pipe32 = Pipe()

    first = Process(target=process1, args=(pipe12,))
    second = Process(target=process2, args=(pipe21, pipe23))
    third = Process(target=process3, args=(pipe32,))

    first.start()
    second.start()
    third.start()

    first.join()
    second.join()
    third.join()
