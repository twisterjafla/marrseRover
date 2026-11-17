from subsystems.camera import camera


class constants:

    testCamName="Laptop Webcam Module (2nd Gen)"
    realCamName=""


    bootConf:list[list[any]] = [ # type: ignore
        [camera, "camera", True]
    ]


    