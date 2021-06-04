import os
import time

class GetCurJointHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  GetCurJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                #Get request from PLC
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'GetCurJoint':
                    print('[Get]  GetCurJoint request.')

                    #Valid
                    joints = '0.0,1.1,2.2,3.3,4.4,5.5;6.6,7.7,8.8,9.9,10.1,11.11;'
                    validcode = 'y' + joints
                    validcode += ' '*(200-len(validcode))
                    os.write(fd,validcode.encode('utf-8'))
                    #Error
                    errorcode = 'n;'
                    errorcode += ' '*(200-len(errorcode))
                    #os.write(fd, errorcode.encode('utf-8'))
                    print('[Sent]  GetCurJoint result.')
                    
            except:
                print('[Error]  GetCurJoint')
            time.sleep(self.interval/2)

if __name__ == '__main__':
    GetCurJoint_Pipepath = '/tmp/GetCurJoint.pipe'
    interval = 0.02
    gcj = GetCurJointHandler(GetCurJoint_Pipepath, interval)
    gcj.runHandler()