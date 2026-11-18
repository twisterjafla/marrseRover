from subsystems.camera import camera


class constants:

    testCamName="Laptop Webcam Module (2nd Gen):"
    realCamName="Arducam OV9782 USB Camera: Ardu"


    bootConf:list[list[any]] = [ # type: ignore
        [camera, "camera", True]
    ]


    