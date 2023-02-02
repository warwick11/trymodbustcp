import socket
import struct
import time
import codecs
import sys
import re

TARGET_IP = '192.168.3.32'
TARGET_PORT = 502
BUFFER_SIZE = 512

pattern=["\\\\x","'","b'",]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TARGET_IP, TARGET_PORT))
sock.settimeout(3.0)
try:
    print("Send modbus request ...")
    transactionId = 6
    protocolId = 0
    len = 6
    unitId = 0x01
    functionCode = 2 # Read Input Status (0x02)
    startRegister = 0x0000
    data = 0x00040  # bit count
    req = struct.pack('>3H 2B 2H', int(transactionId), int(protocolId), int(len), int(unitId), int(functionCode), int(startRegister), int(data))
    sock.send(req)
    rec = sock.recv(BUFFER_SIZE)

    print("TX: {0}".format(codecs.encode(req, 'hex_codec')))
    print("RX: {0}".format(codecs.encode(rec, 'hex_codec')))
    strrec=str(rec)
    di=re.sub('\\\\x','',strrec)
    di=re.sub("b'","",di)
    di=re.sub("'","",di)
    print(di) 

    
    #BIT回収
    di=di[18:]
    #プレフィックス付与
    str_di='0x'+di
    #INT型に変更
    int_di=int(str_di,16)
    #16進数に変kな
    hex_di=hex(int_di)
    #２進数に変換:
    bit_di=bin(hex_di)
    time.sleep(1)
    

finally:
    sock.close()
