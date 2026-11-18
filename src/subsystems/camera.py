
from cv2_enumerate_cameras import enumerate_cameras
import robot
from subsystems.subsystem import subsystem
import cv2
import http.server

class camera(subsystem):
    IP="0.0.0.0"
    PORT=8000
    def __init__(self, parent:"robot.robot", camName:str, shouldServe:bool=True):
        if camName==None: # type: ignore
            self.camera = cv2.VideoCapture(0)
        else:
            hasFound=False

            for i in enumerate_cameras(cv2.CAP_V4L2):   
                print("|"+i.name+"|", camName, i.name==camName)

                if i.name==camName:
                    self.camera=cv2.VideoCapture(i.index)
                    hasFound=True
                    break
                    
            if not hasFound:
                raise RuntimeError('Camera not found!')
            
        self.shouldServe=shouldServe
        


        subsystem.__init__(self, parent, "camera")


    def start(self):
        if self.shouldServe:
            self.httpd= http.server.ThreadingHTTPServer((camera.IP, camera.PORT), lambda Any, _RetAddress, ThreadingHTTPServer : cameraServer(Any,_RetAddress, ThreadingHTTPServer, self)) # type: ignore
            self.httpd.serve_forever()
        super().start()

    def main(self):
        pass



    
    


    def getFrame(self)->bytes:
        success, frame = self.camera.read()
        if not success:
            return None # type: ignore
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


    def kill(self):
        if self.httpd!=None: # type: ignore
            self.httpd.shutdown()
        super().kill()
    



class cameraServer(http.server.BaseHTTPRequestHandler):

    def __init__(self, Any, _RetAddress, ThreadingHTTPServer, host:camera): # type: ignore
        self.camera = host
        super().__init__(Any, _RetAddress, ThreadingHTTPServer) # type: ignore

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        

        try:
            while True:

                frame = self.camera.getFrame()

                if frame!=None: # type: ignore
                    self.wfile.write(b'--frame\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(frame)))
                    self.end_headers()
                    self.wfile.write(frame)

                    
        except Exception as e:
            print("Stream stopped:", e)





