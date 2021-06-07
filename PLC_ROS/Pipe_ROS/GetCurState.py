import os
import time
import rclpy
from rclpy.node import Node

from SysManager.msg import Sysstate


class GetCurStateClient(Node):

    def __init__(self):
        super().__init__('MotionGetCurState')
        self.subscription = self.create_subscription(
            Sysstate, 'sys_state',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self._joint = ''
        self._extjoint = ''

    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.joint)
        self._joint = msg.joint
        self._extjoint = msg.extjoint


class GetCurStateHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.result = ' '
        self.interval = interval
        self.ros_handler = GetCurStateClient()
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  GetCurState: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                #Get request from PLC
                data = os.read(fd,20)
                if data.decode('utf-8').split(';')[0] == 'GetCurState':
                    print('[Get]  GetCurState request.')
                    try:
                        #ROS
                        rclpy.spin_once(self.ros_handler)   
                        
                        print('[Get]  GetCurState result.')
                        #Get data from ROS topic
                        #Valid
                        self.result = str(int(self.ros_handler.state)) + ' '*20
                        self.result = self.result[:20]
                        os.write(fd, self.result.encode('utf-8'))
                    except:
                        #Error
                        self.result = str(int(-2)) + ' '*18
                        os.write(fd, self.result.encode('utf-8'))
                        rclpy.shutdown()
                        rclpy.init()
                        self.ros_handler = GetCurStateClient()
                    print('[Sent]  GetCurState result.')
                    
            except:
                print('[Error]  GetCurState')
            time.sleep(self.interval/2)