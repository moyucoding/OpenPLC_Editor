import os
import time
import threading

import rclpy
from rclpy.executors import ExternalShutdownException,SingleThreadedExecutor
from rclpy.node import Node
from motion.msg import MotionCurJoint

class GetCurJointClient(Node):
    def __init__(self):
        super().__init__('MotionGetCurJoint')
        self.subscription = self.create_subscription(MotionCurJoint, 'MotionCurJoint', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self._joint = [0,0,0,0,0,0]
        self._extjoint = [0,0,0,0,0,0]
    
    def listener_callback(self, msg):
        self._joint = msg.joint
        self._extjoint = msg.extjoint
        

class GetCurJointHandler():
    def __init__(self, path, interval):
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        self.result = ''

        self.executor = SingleThreadedExecutor()
        self.node = GetCurJointClient()
        self.executor.add_node(self.node)

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] GetCurJoint: Pipe: ',self.pipe_path,' exists.')
    
    def rosHandler(self):
        while True:
            try:
                self.executor.spin()
            except ExternalShutdownException:
                try:
                    rclpy.init()
                except:
                    a=1

    def run(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        thread_node = threading.Thread(target=self.rosHandler)
        thread_node.start()
        while True:
            try:
                pipe_raw = os.read(fd, 200)
                if pipe_raw.decode('utf-8').split(';')[0] == 'GetCurJoint':
                    #print('[Info]  GetCurJoint gets request from Pipe.')
                    try:
                        #print('[Info]  GetCurJoint gets result from ROS.')
                        joint = [round(float(x),2) for x in self.node._joint]
                        joint = [str(x) for x in joint]
                        extjoint = [round(float(x),2) for x in self.node._extjoint]
                        extjoint = [str(x) for x in extjoint]

                        self.result = 'y' + ','.join(joint) + ';' + ','.join(extjoint) + ';' + ' '*200
                        self.result = self.result[:200]
                        os.write(fd,self.result.encode('utf-8'))
                        #print('[Info]  GetCurJoint sends result to Pipe.')
                        time.sleep(self.interval)
                    except:
                        time.sleep(self.interval)
            except:
                print('[Error] GetCurJoint.')
            time.sleep(self.interval/2)