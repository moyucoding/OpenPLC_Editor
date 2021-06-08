import os
import time
import threading

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from motion.msg import MotionCurJoint


class GetCurJointClient(Node):

    def __init__(self):
        super().__init__('MotionGetCurJoint')
        self.subscription = self.create_subscription(
            MotionCurJoint, 'MotionCurJoint',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self._joint = [0,0,0,0,0,0]
        self._extjoint = [0,0,0,0,0,0]

    def listener_callback(self, msg):
        self._joint = msg.joint
        self._extjoint = msg.extjoint


class GetCurJointHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.result = ' '
        self.interval = interval
        self.ros_handler = GetCurJointClient()
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.ros_handler)
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  GetCurJoint: Making Pipe: ',self.pipe_path,'.')
    
    def requestHandler(self):
        self.executor.spin()

    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        thread_requsetHandler = threading.Thread(target=self.requestHandler)
        thread_requsetHandler.start()
        while True:
            try:
                #Get request from PLC
                data = os.read(fd,200)
                if data.decode('utf-8').split(';')[0] == 'GetCurJoint':
                    print('[Get]  GetCurJoint request.')
                    try:
                        print('[Get]  GetCurJoint result.')
                        #Get data from handler
                        #Valid
                        joint = [round(float(x),2) for x in self.ros_handler._joint]
                        joint = [str(x) for x in joint]
                        extjoint = [round(float(x),2) for x in self.ros_handler._extjoint]
                        extjoint = [str(x) for x in extjoint]

                        self.result = 'y' + ','.join(joint) + ';' + ','.join(extjoint) + ';' + ' '*200
                        self.result = self.result[:200]
                        os.write(fd, self.result.encode('utf-8'))
                        print('[Sent]  GetCurJoint result.')
                        time.sleep(self.interval)
                    except:
                        #Error
                        self.result = 'n1' +' '*200
                        self.result = self.result[:200]
                        os.write(fd, self.result.encode('utf-8'))
                        print('[Sent]  GetCurJoint result.')
                        time.sleep(self.interval)
                    
                    
                    
            except:
                print('[Error]  GetCurJoint')
            time.sleep(self.interval/2)