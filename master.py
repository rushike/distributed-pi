import threading, socket, sys, time

import config, utils

global server

global wn, wn_buf

global res_str, res_top

global work_task

global RESULT

RESULT  = {}

digit_top = 0

work_task = [0, config.STEP, 2 * config.STEP, 3 * config.STEP,  4 * config.STEP]

work_task = sorted(work_task, reverse = True)

wn = 0

res_str = []

par = None

hxstr = None

res_top = 0

wn_buf = []

wk = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((config.HOST, config.PORT)) 

server.listen(config.WORKERS)

def ms_worker(worker_name, c, addr):
    global server

    global wn, wn_buf, wk

    global res_str, res_top, par, hxstr

    global work_task

    global RESULT
    wn_p = 0
    while True:
        if work_task[-1] > config.PI_RANGE[1]:
            break
        data = c.recv(1024)

        data_str = data.decode('utf8')
        print("DATA RECV : ", data, data_str)
        if config.RES_LOC_PRINT: print("RESULT : ", RESULT)

        if data_str == 'LIVE': #msg for checking if master is alive
            #slave waits for response for while , if master don't responds then first slave to connerct becomes temporary master
            c.send('LIVE')

        if data_str == 'WORK': #need to send work for slave
            #str : function name, args
            if work_task != []:
                func_name = 'PiDI'
                # func_name = 'SQSM'
                digit_top = work_task.pop()
                args = str(digit_top) + "," + str(digit_top + config.STEP) # [) interval
                msg = ("WORK" + func_name + "," + args).encode('utf8')
                print("GIVE WORK : ", msg)
                c.send(msg)


        if data_str.startswith("REST"): #RESULT got 
            # msg = data.decode('utf8')
            _, par, hxstr = data_str.split('|')
            par = tuple(int(v) for v in par.split(","))
            RESULT[par] = hxstr
            top = work_task[0]
            work_task.insert(0, top + config.STEP)
            
        pass
    wk -= 1
    print("\n++++++++++++++++++++++\nEXIT : ", worker_name, c, addr, "\n++++++++++++++++++++++++++++++++++++")
    if wk == 0:
        utils.print_dict(RESULT)
    pass


def connector():
    global server

    global wn, wn_buf, wk

    global res_str, res_top

    global work_task

    log = open("./log.txt", 'a+')
    
    while True : 
        c, addr = server.accept()
        worker_name = "WORKER_" + str(wn)
        log.write(str(c) + "," + str(addr) +  "--->" + worker_name)
        worker = threading.Thread(target = ms_worker, args = (worker_name, c, addr))
        worker.start()
        wn_buf.append((worker_name, c, addr))
        wn += 1
        wk += 1

        if wk == 0: break
        print("wk : ", wk)
        print("Connected to the worker  : ", worker_name)
    
    pass

if __name__ == "__main__":
    con = threading.Thread(target = connector)
    con.start()