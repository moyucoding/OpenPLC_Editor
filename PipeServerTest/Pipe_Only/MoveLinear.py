import os
import time

class MoveLinearHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.ret = ' '*400

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveLinear: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)

        while True:
            try:
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveLinear':
                    print('[Get]  MoveLinear request.')
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)

                    print('[Get]  MoveLinear result.')
                    time.sleep(3)
                    self.ret = 'y' + ' '*399
                    os.write(fd, self.ret.encode('utf-8'))
                    #os.write(fd, 'n1'.encode('utf-8'))
                    print('[Sent]  MoveLinear result.')
                    time.sleep(self.interval)
            except:
                os.write(fd, self.ret.encode('utf-8'))
                print('[ERROR]  MoveLinear.')

            time.sleep(self.interval/2)

if __name__ == '__main__':
    MoveLinear_Pipepath = '/tmp/MoveLinear.pipe'
    interval = 0.02
    mj = MoveLinearHandler(MoveLinear_Pipepath, interval)
    mj.runHandler()