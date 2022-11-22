#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

import cfg

class client:
	def __init__(self,address,values,host="127.0.0.1",port=11000):
		self.host = host
		self.port = port
		self.address = address
		self.values = values
		
	def send(self):
		return SimpleUDPClient(self.host,self.port).send_message(self.address,self.values)
	
def server(ip,port):
	def handler(address, *args):
#		global addr, data, write, beat
		if address != '/live/song/beat': 
			cfg.data = args
			cfg.addr = address
			if cfg.write:
				print(f"{address}: {args}")
		if address == '/live/song/beat':
			cfg.beat = args
			
	dispatcher = Dispatcher()
	dispatcher.map("/live/*", handler)
	server = ThreadingOSCUDPServer((ip, port), dispatcher)
	server.serve_forever()  # Blocks forever
	