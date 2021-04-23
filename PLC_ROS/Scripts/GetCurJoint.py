import os
import time
import rclpy
from rclpy.node import Node

from ros_motion.msg import MotionGetCurJoint


class GetCurJointClient(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            MotionGetCurJoint, 'getcurjoint',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self._result = ''

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.joint)
        self._result = msg.joint


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
                    
                    rclpy.init()
                    self.ros_handler = GetCurJointClient()
                    rclpy.spin_once(self.ros_handler)
                    
                    
                    print('[Get]  GetCurJoint result.')
                    print(self.ros_handler._result)
                    #Get data from ROS topic
                    #Valid
                    joints = [float(x) for x in self.ros_handler._result]
                    str_joints = [str(x) for x in joints]
                    validcode = 'y' + ','.join(str_joints) + ','
                    validcode += ' '*(100-len(validcode))
                    #Error
                    errorcode = 'n1'
                    errorcode  += ' '*(100-len(errorcode))

                    os.write(fd, validcode.encode('utf-8'))
                    #os.write(fd, errorcode.encode('utf-8'))

                    print('[Sent]  GetCurJoint result.')
                    
            except:
                print('[Error]  GetCurJoint')
            time.sleep(0.1)