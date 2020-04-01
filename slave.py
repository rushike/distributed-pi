import socket 
import select 
import sys 

import threading

import config

import time

import pi

#Enrollment Key : DSCE72

global TASK, func, params

params = tuple()
func = None

TASK = None

RES = False

wait = True

RESULT = {}

def connect_to_master(IP_address, Port):
    master = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    master.connect((IP_address, Port)) 
    return master


def speaker(master, typ, *msg):
    if typ == 'WORK':
        message = 'WORK' 
        master.send(message.encode('utf8'))
    if typ == 'REST':
        message = 'REST' + "|" + ','.join(params) + "|" + RES 
        print("SENDING : ", message)
        master.send(message.encode('utf8'))
    pass

def listener(master, SIZE):
    message =  master.recv(SIZE)
    message = message.decode('utf8')
    if message.startswith("WORK"):
        message = message[4:]
        print("message : ", message)
    if message.startswith("WRUP"):
        _, par, hxstr = message.split('|')
        par = tuple(int(v) for v in par.split(","))
        RESULT[par] = hxstr
    return message

def get_func_and_params(mssg:str):
    global func, params
    avail_func_list = {'SQSM': {
                            'paramslen' : 2,
                            'params' : [int, int],
                            'func' : SQSM
                        },
                        'PiDI': {
                            'paramslen' : 2,
                            'params' : [int, int],
                            'func' : PiDI
                        }
                    }
    print("mssg : ", mssg)
    func = avail_func_list[mssg[:4]]['func']
    params = tuple(mssg[5:].split(","))
    return func, params
def SQSM(params):
    start, end = (int(v) for v in  params)
    sm = sum([v * v for v in range(start, end)])
    hex_str = hex(sm)[2:]
    le = len(hex_str)
    print("SQSM : ", hex_str)
    RES = hex_str
    return RES

def PiDI(params):
    start, end = (int(v) for v in  params)
    RES = pi.pi_(start, end)
    return RES

def talk(master):
    # print(TASK)
    global TASK, wait, RES, func, params
    i = 0
    while True:
        
        print("TASK --> ", TASK, ",   RES --> ",RES)
        print("RESULT : ", RESULT)
        if not TASK:
            print("Asking master for : WORK ")
            speaker(master, typ = 'WORK')
            TASK = 'WORK'
        if TASK == 'WORK':
            msg = listener(master, 1024)
            if msg:
                #start the work given if any, else go bye
                func, params = get_func_and_params(msg)
                print("func, param : ", func, params)
                # threading.Thread(target= func, args = params).start()
                RES = func(params)
                pass
        if RES:
            #send result to master
            TASK = None
            print(RES)
            speaker(master, 'REST', RES)

            pass

        i += 1

        # time.sleep(2)

if __name__ == '__main__':
    master = connect_to_master(config.HOST, config.PORT)
    talker = threading.Thread(target = talk, args = (master,))
    talker.start()