import os
import time

import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionJogRotation

class MoveJogRotationClient(Node):
    def __init__(self):
        super().__init__('MotionMoveJogRotation')
        self._action_client = ActionClient(self, MotionJogRotation, 'Motion/MoveJogRotation')
        self._ret = 0
    
    def send_goal(self, goal_msg):
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        

class MoveJogRotationHandler():
    def __init__(self, path, interval):
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        self.goal = MotionJogRotation.Goal()
        self.result = ''

        self.node = MoveJogRotationClient()

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] MoveJogRotation: Pipe: ',self.pipe_path,' exists.')
    
    def rosHandler(self):
        try:
            self.node.send_goal(self.goal)
            print('[Info]  MoveJogRotation sends request to ROS.')
        except:
            rclpy.shutdown()
            rclpy.init()
            self.node = MoveJogRotationClient()

    def run(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                pipe_raw = os.read(fd, 200)
                if pipe_raw.decode('utf-8').split(';')[0] == 'MoveJogRotation':
                    print('[Info]  MoveJogRotation gets request from Pipe.')
                    try:
                        pipe_msg = pipe_raw.decode('utf-8').split(';')[1:-1]
                        
                        self.goal = MotionJogRotation.Goal()
                        self.goal.id = 1
                        self.goal.user = [1.0] + [0.0] * 6
                        self.goal.tool = [0.0] * 7
                        self.goal.jogtype = int(pipe_msg[0])

                        load = [float(x) for x in pipe_msg[1].split(',')[:]]
                        self.goal.load = [0.0] * 10
                        for i in range(len(load)):
                            self.goal.load[i] = load[i]

                        self.goal.speed = float(pipe_msg[2])
                    
                        self.rosHandler()

                    except:
                        time.sleep(self.interval)
            except:
                print('[Error] MoveJogRotation.')
            time.sleep(self.interval/2)