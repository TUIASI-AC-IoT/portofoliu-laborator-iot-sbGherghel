import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.30"
PEER_PORT = 10001



i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        toggle=i%2
        msg0 = "GPIO4="+str(toggle)
        TO_SEND = msg0.encode("ascii") # + bytes(str(toggle),"ascii")
        sock.sendto(TO_SEND, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", TO_SEND)
        i = i + 1
        time.sleep(1)
    except KeyboardInterrupt:
        break