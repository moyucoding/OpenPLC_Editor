import os
import time
import threading

class MoveJogRotationHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.request = ''
        self.count = 0
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJogRotation: Making Pipe: ',self.pipe_path,'.')
    
    def requestHandler(self):
        msg = self.request.split(';')[1:-1]
        print(msg)
        time.sleep(1)
        self.count +=1
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        count = 0
        while True:
            try:
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'MoveJogRotation':
                    count += 1
                    print('[Get]  MoveJogRotation request.', count, self.count)
                    self.request = data.decode('utf-8')
                    thread_requestHandeler = threading.Thread(target=self.requestHandler)
                    thread_requestHandeler.start()
            except:
                print('[ERROR]  MoveJogRotation.')

            time.sleep(self.interval/2)

if __name__ == '__main__':
    MoveJogRotation_Pipepath = '/tmp/MoveJogRotation.pipe'
    interval = 0.02
    mj = MoveJogRotationHandler(MoveJogRotation_Pipepath, interval)
    mj.runHandler()