import os
import time

class ErrorRecoverHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  ErrorRecover: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        count = 0
        while True:
            try:
                data = os.read(fd, 20)
                if data.decode('utf-8').split(';')[0] == 'ErrorRecover':
                    count += 1
                    print('[Get]  ErrorRecover request.', count)
                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    print(msg)
                    #
                    #print('[Get]  ErrorRecover result.')
                    time.sleep(0.1)
            except:
                print('[ERROR]  ErrorRecover.')

            time.sleep(0.01)

if __name__ == '__main__':
    ErrorRecover_Pipepath = '/tmp/ErrorRecover.pipe'
    mj = ErrorRecoverHandler(ErrorRecover_Pipepath)
    mj.runHandler()