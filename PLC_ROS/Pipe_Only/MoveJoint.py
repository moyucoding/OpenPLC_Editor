import os
import time

class MoveJointHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)

        while True:
            try:
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveJoint':
                    print('[Get]  MoveJoint request.')
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)
                    #

                    print('[Get]  MoveJoint result.')
                    time.sleep(1)
                    os.write(fd, 'y '.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    print('[Sent]  MoveJoint result.')
            except:
                print('[ERROR]  MoveJoint.')

            time.sleep(0.1)

if __name__ == '__main__':
    MoveJoint_Pipepath = '/tmp/MoveJoint.pipe'
    mj = MoveJointHandler(MoveJoint_Pipepath)
    mj.runHandler()