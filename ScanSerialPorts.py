import serial.tools.list_ports
import time


def main():
    while True:
        print("------------------")
        ports = [port.device for port in serial.tools.list_ports.comports()]
        for port in ports:
            if 'cu.usbserial' in port:
                print(port)
        time.sleep(1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
