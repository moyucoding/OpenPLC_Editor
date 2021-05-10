import os
import time
import rclpy
from rclpy.node import Node

from motion.msg import MotionCurJoint


class GetCurJointClient(Node):

    def __init__(self):
        super().__init__('MotionGetCurJoint')
        self.subscription = self.create_subscription(
            MotionGetCurJoint, 'MotionCurJoint',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self._joint = ''
        self._extjoint = ''

    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.joint)
        self._joint = msg.joint
        self._extjoint = msg.extjoint


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
                data = os.read(fd,20)
                if data.decode('utf-8').split(';')[0] == 'GetCurJoint':
                    print('[Get]  GetCurJoint request.')
                    try:
                        #ROS
                        rclpy.init()
                        self.ros_handler = GetCurJointClient()
                        rclpy.spin_once(self.ros_handler)   
                        rclpy.shutdown()                 
                        print('[Get]  GetCurJoint result.')

                        #Get data from ROS topic
                        #Valid
                        joint = [round(float(x),2) for x in self.ros_handler._joint]
                        joint = [str(x) for x in joint]
                        extjoint = [round(float(x),2) for x in self.ros_handler._extjoint]
                        extjoint = [str(x) for x in extjoint]

                        validcode = 'y' + ','.join(joint) + ';' + ','.join(extjoint) + ';'
                        validcode += ' '*(200-len(validcode))
                        os.write(fd, validcode.encode('utf-8'))
                    except:
                        #Error
                        errorcode = 'n1'
                        errorcode  += ' '*(200-len(errorcode))
                        os.write(fd, errorcode.encode('utf-8'))
                    
                    print('[Sent]  GetCurJoint result.')
                    
            except:
                print('[Error]  GetCurJoint')
            time.sleep(0.1)