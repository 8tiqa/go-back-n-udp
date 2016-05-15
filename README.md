# BadNet
Python Implementation of the Go-back-N protocol for file transfer using Client server communication over UDP. 


# RDT Technologies Details
The client transfers a single file to the server's local directory over UDP on a _VERY_ unreliable network. It begins with reading chunks of data from a file and sending them as packets (packetsize < 1KB) to the server that acknowledges the packets received.
The catch is that the client program can send multiple packets to the server without waiting for an acknowledgment but is constrained to maintain a window of size N over a range of sequence numbers of unacknowledged packets. The lower bound 'base' is the sequence number of the oldest unacknowledged packet and the upper bound is the total windowSize. It also maintains the nextSeqnum that is defined to be the sequence number of the packet to be sent. On the other hand, the server program maintains the sequence number of the next in-order packet only.

To combat the unreliability of the network, this protocol incorporates the use of sequence numbers, commulative acknowledgements, checksums, and a timeout/retransmit operation. 

If a packet is dropped, duplicated or delivered out of order,
the Seqnum of the packets received will be out of order- that is the expected seqnum and the received seqnum mismatch. The Server discards the out of order packet and resends an ACK for the most recently received in-order packet. A timeout event occurs at the Client which leads to retransmission of all the packets that have been sent but have not been acknowledged yet.

If a single bit error is created within a packet,
the value of Checksum indicates that the packet is corrupted. The Client program calculates the checksum on the data using the hash library and appends the calculated value to the packet sent. The Server program extracts this checksum value, recalculates the checksum on the received data and compares the two values. If the packet is corrupted, the server discards the packet and resends the last ACK. This leads to retransmission of the corrupted packet from the client side.
