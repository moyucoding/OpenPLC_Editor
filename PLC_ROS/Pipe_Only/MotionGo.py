import os
import time 


class MotionGoHandler():
    def __init__(self, path) -> None:
        #super().__init__()
        self.pipe_path = path
        self.result = ''
        
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MotionGo: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        
        while True:
            try:
                data = os.read(fd, 10)
                if data.decode('utf-8').split(';')[0] == 'MotionGo':
                    print('[Get]  MotionGo request.')

                    print('[Get]  MotionGo result.')
                    time.sleep(1)
                    ret = '1'
                    os.write(fd, ret.encode('utf-8'))
                    print('[Sent]  MotionGo result.')
            except:
                print('[ERROR]  MotionGo.')

            time.sleep(0.1)


if __name__ == '__main__':
    MotionGo_Pipepath = '/tmp/MotionGo.pipe'
    go = MotionGoHandler(MotionGo_Pipepath)
    go.runHandler()