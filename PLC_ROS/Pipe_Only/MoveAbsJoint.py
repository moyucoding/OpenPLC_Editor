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
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveAbsJoint':
                    print('[Get]  MoveAbsJoint request.')
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)
                    #

                    print('[Get]  MoveAbsJoint result.')
                    time.sleep(1)
                    os.write(fd, 'y '.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    print('[Sent]  MoveAbsJoint result.')
            except:
                print('[ERROR]  MoveAbsJoint.')

            time.sleep(0.1)

if __name__ == '__main__':
    MoveAbsJoint_Pipepath = '/tmp/MoveAbsJoint.pipe'
    maj = MoveAbsJointHandler(MoveAbsJoint_Pipepath)
    maj.runHandler()