import os
import time
import threading

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sysmanager.action import ErrorRecover

class ErrorRecoverActionClient(Node):

    def __init__(self):
        super().__init__('SysManagerErrorRecover')
        self._action_client = ActionClient(self, ErrorRecover, 'SysManager/ErrorRecover')
        self._ret = 0

    def send_goal(self, goal_msg):
        goal_msg = ErrorRecover.Goal()
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        

class ErrorRecoverHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.request = ''
        self.count = 0
        self.ros_handler = ErrorRecoverActionClient()

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
                    print('[Get]  ErrorRecover request.  Get:',count)
                    goal = ErrorRecover.Goal()
                    try:
                        self.ros_handler.send_goal(goal)
                    except:
                        rclpy.shutdown()
                        rclpy.init()
                        self.ros_handler = ErrorRecoverActionClient()
            except:
                print('[Error]  ErrorRecover.')
            time.sleep(self.interval/2)
