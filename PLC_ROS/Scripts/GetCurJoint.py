import os
import time

class GetCurJointHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  GetCurJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                #Get request from PLC
                data = os.read(fd,100)
                if data.decode('utf-8') == 'g' :
                    print('[Get]  GetCurJoint request.')
                    #
                    # Do Something
                    # 
                    #Get data from ROS topic
                    #Valid
                    axises = '111.0,1.1,2.2,3.3,4.4,5.5,'
                    validcode = 'y' + axises
                    validcode += ' '*(100-len(validcode))
                    #Error
                    errorcode = 'n1'
                    errorcode  += ' '*(100-len(errorcode))
                    

                    print('[Get]  GetCurJoint result.')
                    time.sleep(10)
                    #os.write(fd, validcode.encode('utf-8'))
                    os.write(fd, errorcode.encode('utf-8'))
            except:
                print('[Error]  GetCurJoint')
            time.sleep(0.1)