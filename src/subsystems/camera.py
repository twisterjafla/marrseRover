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
        self.camera = cv2.VideoCapture(0)
        self.shouldServe=shouldServe
        


        subsystem.__init__(self, "camera")


    def start(self):
        if self.shouldServe:
            self.httpd= http.server.ThreadingHTTPServer((camera.IP, camera.PORT), lambda Any, _RetAddress, ThreadingHTTPServer : cameraServer(Any,_RetAddress, ThreadingHTTPServer, self)) # type: ignore
            self.httpd.serve_forever()
        super().start()

    def main(self):
        if self.shouldServe:
            frame=self.getFrame

            if frame!=None: 
                self.httpd.ser

    
    


    def getFrame(self)->bytes:
        success, frame = self.camera.read()
        if not success:
            return None # type: ignore
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


    def kill(self):
        if self.httpd!=None:
            self.httpd.shutdown()
        super().kill()
    



class cameraServer(http.server.BaseHTTPRequestHandler):

    def __init__(self, Any, _RetAddress, ThreadingHTTPServer, host:camera):
        self.camera = host
        super().__init__(Any, _RetAddress, ThreadingHTTPServer)

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        

        try:
            while True:

                frame = self.camera.getFrame()

                if frame!=None:
                    self.wfile.write(b'--frame\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)

                    
        except Exception as e:
            print("Stream stopped:", e)





