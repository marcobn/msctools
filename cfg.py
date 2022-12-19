#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

addr = None 
data = None
source_addr = None 
source_data = None

write = False
beat = None
tempo = 60.0

NTRACK = 128
stop = [False]*NTRACK
stop_source = [False]*NTRACK
sleep = [0]*NTRACK
beat = [1]*NTRACK

TICK = 0.15
CLOCK = TICK/10
PORT = 11000
COMM_A = 18080
COMM_B = 18081
COMM_C = 18082
COMM_D = 18083
HOST = "127.0.0.1"
