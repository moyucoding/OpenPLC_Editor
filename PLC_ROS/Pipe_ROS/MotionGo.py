import os
import time 

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from ros_motion.action import MotionGo


class MotionGoActionClient(Node):

    def __init__(self):
        super().__init__('Motion/Go')
        self._action_client = ActionClient(self, MotionGo, 'Motion/Go')
        self._action_result = 0

    def send_goal(self):
        goal_msg = MotionGo.Goal()
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.ret))
        self._action_result = result.ret
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = 1





class MotionGoHandler():
    def __init__(self, path) -> None:
        #super().__init__()
        self.pipe_path = path
        self.result = ''
        
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MotionGo: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        
        while True:
            try:
                data = os.read(fd, 10)
                if data.decode('utf-8').split(';')[0] == 'MotionGo':
                    print('[Get]  MotionGo request.')
                    rclpy.init()
                    self.ros_handler = MotionGoActionClient()
                    self.ros_handler.send_goal()
                    rclpy.spin(self.ros_handler)
                    print('[Get]  MotionGo result.')
                    if(self.ros_handler._action_result == 1):
                        os.write(fd, '1'.encode('utf-8'))
                        print('[Sent]  MotionGo result.')
            except:
                print('[ERROR]  MotionGo.')
                rclpy.shutdown()

            time.sleep(0.1)


