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
stop_A = False
stop_B = False
stop_C = False
stop_D = False
stop_score = False
stop_source = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,\
               False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
sleepA = 0
sleepB = 0
sleepC = 0
sleepD = 0
sleep_score = 0
beatA = 1
beatD = 1
beat_score = 1
TICK = 0.15
CLOCK = TICK/10
PORT = 11000
COMM_A = 18080
COMM_B = 18081
COMM_C = 18082
COMM_D = 18083
HOST = "127.0.0.1"
