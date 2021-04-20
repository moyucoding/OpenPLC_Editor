import os
import time 

from action_msgs.msg import GoalStatus
from example_interfaces.action import Fibonacci

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class MotionGoActionClient(Node):

    def __init__(self):
        super().__init__('motiongo_action_client')
        
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: {0}'.format(result.sequence))
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(status))
        # Shutdown after receiving a result
        rclpy.shutdown()

    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)




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
                data = os.read(fd, 1)
                if data.decode('utf-8') == 'g':
                    print('[Get]  MotionGo request.')
                    #
                    # Do Something
                    # 
                    rclpy.init()
                    self.ros_handler = MotionGoActionClient()
                    self.ros_handler.send_goal()
                    rclpy.spin(self.ros_handler)
                    print('[Get]  MotionGo result.')
                    os.write(fd, 's'.encode('utf-8'))
                    print('[Sent]  MotionGo result.')
                    #print('[Get]  MotionGo result.')
                    #os.write(fd, 's'.encode('utf-8'))
            except:
                print('[ERROR]  MotionGo.')

            time.sleep(0.1)


