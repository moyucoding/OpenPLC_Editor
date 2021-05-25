import os
import time 


class RobotEnableHandler():
    def __init__(self, path) -> None:
        #super().__init__()
        self.pipe_path = path
        self.result = ''
        
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  RobotEnable: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        
        while True:
            try:
                data = os.read(fd, 20)
                data_strs = data.decode('utf-8').split(';')
                if data_strs[0] == 'RobotEnable':
                    if data_strs[1] == '1':
                        print('[Get]  RobotEnable request.')
                        print('Enabling')
                        print('[Get]  RobotEnable result.')
                        time.sleep(1)
                        ret = '1'
                        os.write(fd, ret.encode('utf-8'))
                        print('[Sent]  RobotEnable result.')
                    elif data_strs[1] == '0':
                        print('[Get]  RobotEnable request.')
                        print('Disabling')
                        print('[Get]  RobotEnable result.')
                        time.sleep(1)
                        ret = '1'
                        os.write(fd, ret.encode('utf-8'))
                        print('[Sent]  RobotEnable result.')
            except:
                print('[ERROR]  RobotEnable.')

            time.sleep(0.1)


if __name__ == '__main__':
    RobotEnable_Pipepath = '/tmp/RobotEnable.pipe'
    go = RobotEnableHandler(RobotEnable_Pipepath)
    go.runHandler()