import threading, socket, sys

import config

global server

global wn, wn_buf

wn_buf = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((config.HOST, config.PORT)) 

server.listen(config.WORKERS)

def ms_worker(worker_name, c, addr):
    wn_p = 0
    while True:
        data = c.recv(1024)

        if data == 'LIVE': #msg for checking if master is alive
            #slave waits for response for while , if master don't responds then first slave to connerct becomes temporary master
            c.send('LIVE')


        if wn_p != wn: #update everyones currently working list
            #send the last value to slave worker where he will update its own list
            #brodcasting WRUP -- worker update
            c.send("WRUP" + str(worker_name) + "," + str(addr))
            pass
        pass
    pass


def connector():
    log = open("./log.txt", 'a+')
    
    while True : 
        c, addr = server.accept()
        worker_name = "WORKER_" + str(wn)
        log.write(str(c) + "," + str(addr), "--->" + worker_name)
        worker = threading.Thread(target = ms_worker, args = (worker_name, c, addr))
        worker.start()
        
        wn_buf.append((worker_name, c, addr))
        wn += 1
    pass



# connector()