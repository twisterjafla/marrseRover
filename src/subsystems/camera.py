import typing
from subsystems.subsystem import subsystem
import cv2
import numpy
import http.server
import socketserver
import cv2
import io
import socket

class camera(subsystem):
    IP="0.0.0.0"
    PORT=8000
    def __init__(self, shouldServe:bool=True):
        subsystem.__init__(self, "camera")
        self.camera = cv2.VideoCapture(0)
        self.shouldServe=shouldServe
        
        if shouldServe:
            self.server=cameraServer
        else:
            self.server=None

    def start(self):
        if self.shouldServe:
            self.httpd= http.server.ThreadingHTTPServer((camera.IP, camera.PORT), self.server) # type: ignore
            self.httpd.serve_forever()

        super().start()

    def main(self):
        if self.shouldServe:
            frame=self.getFrame

            if frame!=None: 
                self.server.push(frame)

    


    def getFrame(self)->bytes:
        success, frame = self.camera.read()
        if not success:
            return None # type: ignore
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    



class cameraServer(http.server.BaseHTTPRequestHandler):

    def __init__(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

    def push(self, frame:bytes):
        self.wfile.write(b'--frame\r\n')
        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', len(frame))
        self.end_headers()
        self.wfile.write(frame)


