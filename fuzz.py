# Author: Marc Hortelano
## Template fuzzing BoF
#####
# If you have ssh conection and the bof is runing on localhost run: ssh user@ip -L 127.0.0.1:lport:127.0.0.1:rport
#####


#!/usr/bin/python3

import socket
import sys
import time
from pwn import *

## Change this part
host = '' # IP  
port = '' # PORT 

#usern = b'' # First comand
pre_buf = b' ' # Comand




# Don't change
timeout = 5


if __name__ == '__main__':

    p1 = log.progress("BoF")
    p1.status("Connecting ...")
    p2 = log.progress("Reply")
    
    length = 100 #inital length of bytes to send to binary
    
    while (length < 10000): #continue to send data until bytes == 10000 
        try:    
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((host, int(port))) #Connect to host
            reply = s.recv(1024) #Grab banners (if any)
          
            p2.status("Banner: {}".format(str(reply.decode().strip())))
#            s.send(usern) # send first comand
            time.sleep(2)
            s.send(pre_buf + b"A" * length) #Send payload
            reply = s.recv(1024)
            p2.status("Response: {}".format(str(reply.decode().strip())))
            s.close()
        except:
            p1.success("BoF find : {}".format(str(length)))
            sys.exit(0)

        time.sleep(2)
        p1.status("Buffer sent: {}".format(str(length)))
        length += 100 #increment payload by 100
   
    p1.failure("BoF not find ...")
    p2.failure("No reply ...")
