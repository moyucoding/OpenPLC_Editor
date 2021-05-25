import os
import time

class GetCurStateHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

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
                    ret = '1'
                    os.write(fd,ret.encode('utf-8'))
                    print('[Sent]  GetCurState result.')
                    time.sleep(0.1)
            except:
                print('[Error]  GetCurState')
            time.sleep(0.001)

if __name__ == '__main__':
    GetCurState_Pipepath = '/tmp/GetCurState.pipe'
    gcj = GetCurStateHandler(GetCurState_Pipepath)
    gcj.runHandler()