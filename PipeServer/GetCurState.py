import os
import time
import threading

import rclpy
from rclpy.executors import ExternalShutdownException, SingleThreadedExecutor
from rclpy.node import Node
from sysmanager.msg import Sysstate

class GetCurStateClient(Node):
    def __init__(self):
        super().__init__('MotionGetCurState')
        self.subscription = self.create_subscription(Sysstate, 'sys_state', self.listener_callback, 10)
        #self.subscription  # prevent unused variable warning
        self.state = -2
    
    def listener_callback(self, msg):
        self.state = int(msg.state)
        

class GetCurStateHandler():
    def __init__(self, path, interval):
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        self.result = ''

        self.executor = SingleThreadedExecutor()
        self.node = GetCurStateClient()
        self.executor.add_node(self.node)

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] GetCurState: Pipe: ',self.pipe_path,' exists.')
    
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
                pipe_raw = os.read(fd, 20)
                if pipe_raw.decode('utf-8').split(';')[0] == 'GetCurState':
                    #print('[Info]  GetCurState gets request from Pipe.')
                    try:
                        #print('[Info]  GetCurState gets result from ROS.')
                        self.result = str(int(self.node.state)) + ' '*20
                        self.result = self.result[:20]
                        os.write(fd,self.result.encode('utf-8'))
                        #print('[Info]  GetCurState sends result to Pipe.')
                        time.sleep(self.interval)
                    except:
                        time.sleep(self.interval)
            except:
                print('[Error] GetCurState.')
            time.sleep(self.interval/2)