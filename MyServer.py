from socket import *
from BadNet5 import *
import pickle
import hashlib
import sys
import os
import math
import time

#takes the port number as command line arguments and create server socket
serverIP="127.0.0.1"
serverPort=int(sys.argv[1])

serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind((serverIP,serverPort))
serverSocket.settimeout(3)
print "Ready to serve"

#initializes packet variables 
expectedseqnum=1
ACK=1
ack = []

#RECEIVES DATA
f = open("output", "wb")
endoffile = False
lastpktreceived = time.time()	
starttime = time.time()

while True:

	try:
		rcvpkt=[]
		packet,clientAddress= serverSocket.recvfrom(4096)
		rcvpkt = pickle.loads(packet)
#		check value of checksum received (c) against checksum calculated (h) - NOT CORRUPT
		c = rcvpkt[-1]
		del rcvpkt[-1]
		h = hashlib.md5()
		h.update(pickle.dumps(rcvpkt))
		if c == h.digest():
#		check value of expected seq number against seq number received - IN ORDER 
			if(rcvpkt[0]==expectedseqnum):
				print "Received inorder", expectedseqnum
				if rcvpkt[1]:
					f.write(rcvpkt[1])
				else:
					endoffile = True
				expectedseqnum = expectedseqnum + 1
#				create ACK (seqnum,checksum)
				sndpkt = []
				sndpkt.append(expectedseqnum)
				h = hashlib.md5()
				h.update(pickle.dumps(sndpkt))
				sndpkt.append(h.digest())
				BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
				print "New Ack", expectedseqnum

			else:
#		default? discard packet and resend ACK for most recently received inorder pkt
				print "Received out of order", rcvpkt[0]
				sndpkt = []
				sndpkt.append(expectedseqnum)
				h = hashlib.md5()
				h.update(pickle.dumps(sndpkt))
				sndpkt.append(h.digest())
				BadNet.transmit(serverSocket, pickle.dumps(sndpkt), clientAddress[0], clientAddress[1])
				print "Ack", expectedseqnum
		else:
			print "error detected"
	except:
		if endoffile:
			if(time.time()-lastpktreceived>3):
				break


endtime = time.time()

f.close()
print 'FILE TRANFER SUCCESSFUL'
print "TIME TAKEN " , str(endtime - starttime)
