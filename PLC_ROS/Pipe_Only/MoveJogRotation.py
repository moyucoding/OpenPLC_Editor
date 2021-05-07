import os
import time

class MoveJogRotationHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJogRotation: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        count = 0
        while True:
            try:
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'MoveJogRotation':
                    count += 1
                    print('[Get]  MoveJogRotation request.', count)
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)
                    #
                    #print('[Get]  MoveJogRotation result.')
                    time.sleep(1)
                    #os.write(fd, 'y '.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    #print('[Sent]  MoveJogRotation result.')
            except:
                print('[ERROR]  MoveJogRotation.')

            time.sleep(0.01)

if __name__ == '__main__':
    MoveJogRotation_Pipepath = '/tmp/MoveJogRotation.pipe'
    mj = MoveJogRotationHandler(MoveJogRotation_Pipepath)
    mj.runHandler()