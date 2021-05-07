import os
import time

class MoveJogJointHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJogJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        count = 0
        while True:
            try:
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'MoveJogJoint':
                    count += 1
                    print('[Get]  MoveJogJoint request.', count)
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)
                    #
                    #print('[Get]  MoveJogJoint result.')
                    time.sleep(1)
                    #os.write(fd, 'y '.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    #print('[Sent]  MoveJogJoint result.')
            except:
                print('[ERROR]  MoveJogJoint.')

            time.sleep(0.01)

if __name__ == '__main__':
    MoveJogJoint_Pipepath = '/tmp/MoveJogJoint.pipe'
    mj = MoveJogJointHandler(MoveJogJoint_Pipepath)
    mj.runHandler()