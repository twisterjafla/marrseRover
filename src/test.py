#temp file for testing use. Can and will be overwritten.

import time
from constants import constants
from subsystems.camera import camera

def main():
    camera(None, constants.realCamName)
    while True:
        time.sleep(1)



if __name__=="__main__":
    main()
    # while True:
    #     time.sleep(1)
       
