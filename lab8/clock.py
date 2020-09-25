from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

# def local_time(counter):
#     return '(LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,datetime.now())

def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1

def event(pid, counter):
    counter += 1
    print('Something happened in {}!'.format(pid))
    return counter

def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid))
    return counter

def recieve_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid))
    return counter

def process1(pipe12):
    pid = getpid()
    print('Process 1 has ID ', pid)
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter  = event(pid, counter)
    counter = recieve_message(pipe12, pid, counter)
    counter  = event(pid, counter)

def process2(pipe21, pipe23):
    pid = getpid()
    print('Process 2 has ID ', pid)
    counter = 0
    counter = send_message(pipe23, pid, counter)
    counter = recieve_message(pipe23, pid, counter)
    counter = recieve_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    

def process3(pipe32):
    pid = getpid()
    print('Process 3 has ID ', pid)
    counter = 0
    counter = recieve_message(pipe32, pid, counter)
    counter = send_message(pipe32, pid, counter)

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