import os
import time

class MoveAbsJointHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveAbsJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                data = os.read(fd, 500)
                if data.decode('utf-8')!='y0' :
                    print('[Get]  MoveAbsJoint request.')
                    print(data.decode('utf-8'))
                    #
                    # Do Something
                    # 
                    print('[Get]  MoveAbsJoint result.')
                    os.write(fd,'yf0'.encode('utf-8'))
            except:
                print('[Error]  MoveAbsJoint')
            time.sleep(0.1)