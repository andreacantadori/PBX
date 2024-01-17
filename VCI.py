import serial 
import serial.tools.list_ports
import socket
import sys
import random
import select

def randomBinaryString():
    return ''.join([hex(random.randint(0,255))+' ' for i in range(random.randint(1,8))])

#------------------------------------------------------------
def start_client(ip, port, comPort):

    ser = serial.Serial(comPort, 921600, timeout=0)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5.0)
    client_socket.setblocking(False)
    
    connected = False
    try:
        client_socket.connect((ip, port))
    except socket.timeout as e:
        print(f"[*] Timeout: {str(e)}")
    except socket.error as e:
        if e.errno == socket.errno.EINPROGRESS:
            # Connection is in progress, use select to wait for it to complete
            _, writable, _ = select.select([], [client_socket], [], 5.0)
            if client_socket in writable:
                print(f"[*] Connected to {ip}:{port}")
                connected = True
            else:
                print("Connection failed")
        else:
            print(f"[*] Error: {str(e)}")

    if connected:
        keepLooping = True
        try:
            client_socket.settimeout(0.0)
            client_socket.setblocking(False)
            while keepLooping:
                try:
                    data = client_socket.recv(128)
                    if len(data) > 0:
                        ser.write(data)
                        #ser.flush()
                        #hex_representation = ' '.join(f'{byte:02x}' for byte in data)
                        #print(f"From server: {hex_representation}")
                except socket.error as e:
                    pass
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting)
                    client_socket.send(data)
                    #hex_representation = ' '.join(f'{byte:02x}' for byte in data)
                    #print(f"From serial: {hex_representation}")
        except socket.timeout as e:
            print(f"[*] Timeout: {str(e)}")
        except socket.error as e:
            if e.errno == socket.errno.EINPROGRESS:
                # Connection is in progress, use select to wait for it to complete
                _, writable, _ = select.select([], [client_socket], [], 5.0)
                if client_socket in writable:
                    # Connection successful
                    print("Connected")
                else:
                    # Connection failed
                    print("Connection failed")
            else:
                print(f"[*] Error: {str(e)}")
        client_socket.close()
        ser.close()


if __name__ == "__main__":
    #start_client("ec2-18-193-222-202.eu-central-1.compute.amazonaws.com", 40000, "/dev/cu.usbserial-01FDFFE4")
    if len(sys.argv) > 3:
        start_client(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("Missing arguments: <IP> <port> <com_port>")

