import os
import time

class MoveCircleHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.ret = ' '*400

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveCircle: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)

        while True:
            try:
                data = os.read(fd, 500)
                if data.decode('utf-8').split(';')[0] == 'MoveCircle':
                    print('[Get]  MoveCircle request.')
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)

                    print('[Get]  MoveCircle result.')
                    time.sleep(3)
                    ret = 'y' + ' '*499
                    os.write(fd, ret.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    print('[Sent]  MoveCircle result.')
                    time.sleep(self.interval)
            except:
                os.write(fd, self.ret.encode('utf-8'))
                print('[ERROR]  MoveCircle.')

            time.sleep(self.interval)

if __name__ == '__main__':
    MoveCircle_Pipepath = '/tmp/MoveCircle.pipe'
    interval = 0.02
    mj = MoveCircleHandler(MoveCircle_Pipepath, interval)
    mj.runHandler()