import os
import time
import threading

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionJogLinear

class MoveJogLinearActionClient(Node):

    def __init__(self):
        super().__init__('MotionMoveJogLinear')
        self._action_client = ActionClient(self, MotionJogLinear, 'Motion/MoveJogLinear')
        self._ret = 0

    def send_goal(self, goal_msg):
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)


class MoveJogLinearHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.request = ''
        self.count = 0
        self.ros_handler = MoveJogLinearActionClient()
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJogLinear: Making Pipe: ',self.pipe_path,'.')
    
    def requestHandler(self):
        msg = self.request.split(';')[1:-1]
        #Create a goal
        goal = MotionJogLinear.Goal()
        goal.id = 1
        goal.user = [1.0] + [0.0] * 6
        goal.tool = [0.0] * 7
        goal.jogtype = int(msg[0])
        
        load = [float(x) for x in msg[1].split(',')[:]]
        goal.load = [0.0] * 10
        for i in range(len(load)):
            goal.load[i] = load[i]
        
        goal.speed = float(msg[2])
        try:
            self.ros_handler.send_goal(goal)
        except:
            rclpy.shutdown()
            rclpy.init()
            self.ros_handler = MoveJogLinearActionClient()
        self.count += 1

    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        count = 0
        while True:
            try:
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'MoveJogLinear':
                    count += 1
                    print('[Get]  MoveJogLinear request.  Get:',count, ' Sent:',self.count)
                    self.request = data.decode('utf-8')
                    thread_requestHandeler = threading.Thread(target=self.requestHandler)
                    thread_requestHandeler.start()
            except:
                print('[Error]  MoveJogLinear.')
            time.sleep(self.interval/2)