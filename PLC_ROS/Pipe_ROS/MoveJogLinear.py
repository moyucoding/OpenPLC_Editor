import os
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ros_motion.action import MotionMoveJogLinear

class MoveJogLinearActionClient(Node):

    def __init__(self):
        super().__init__('Motion/MoveJogLinear')
        
        self._action_client = ActionClient(self, MotionMoveJogLinear, 'Motion/MoveJogLinear')
        self._ret = 0

    def send_goal(self, goal_msg):
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
        rclpy.shutdown()




class MoveJogLinearHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJogLinear: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                data = os.read(fd, 200)
                if data.decode('utf-8').split(';')[0] == 'MoveJogLinear':
                    print('[Get]  MoveJogLinear request.')

                    request = data.decode('utf-8')
                    msg = request.split(';')[1:-1]
                    #Create a goal
                    goal = MotionMoveJogLinear.Goal()
                    goal.id = 1
                    goal.jogtype = int(msg[0])
                    goal.load = [float(x) for x in msg[1].split(',')[:]]
                    goal.speed = float(msg[2])
                    
                    rclpy.init()
                    self.ros_handler = MoveJogLinearActionClient()
                    self.ros_handler.send_goal(goal)
                    print('[Sent]  MoveJogLinear request.')

            except:
                print('[Error]  MoveJogLinear')
            time.sleep(0.1)