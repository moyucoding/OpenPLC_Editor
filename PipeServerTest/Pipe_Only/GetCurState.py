import os
import time

class GetCurStateHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  GetCurState: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                #Get request from PLC
                data = os.read(fd, 20)
                if data.decode('utf-8').split(';')[0] == 'GetCurState':
                    print('[Get]  GetCurState request.')
                    ret = '1' + ' '*19
                    os.write(fd,ret.encode('utf-8'))
                    print('[Sent]  GetCurState result.')
            except:
                print('[Error]  GetCurState')
            time.sleep(self.interval/2)

if __name__ == '__main__':
    GetCurState_Pipepath = '/tmp/GetCurState.pipe'
    interval = 0.02
    gcj = GetCurStateHandler(GetCurState_Pipepath, interval)
    gcj.runHandler()