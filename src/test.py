#temp file for testing use. Can and will be overwritten.

import time
from subsystems.camera import camera

def main():
    camera("Laptop Webcam Module (2nd Gen)")
    while True:
        time.sleep(1)



if __name__=="__main__":
    main()
    # while True:
    #     time.sleep(1)
       
