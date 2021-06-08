import os
import time 

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from driver.action import DriverWriteSdi

class RobotEnableActionClient(Node):

    def __init__(self):
        super().__init__('RobotEnable')
        self._action_client = ActionClient(self, DriverWriteSdi, 'Driver_Write_Sdi')
        self._ret = 0

    def send_goal(self, goal_msg):
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
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
        self._ret = result.ret
        rclpy.shutdown()


class RobotEnableHandler():
    def __init__(self, path, interval) -> None:
        #super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.result = ' '
        
        self.goal = DriverWriteSdi.Goal()
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  RobotEnable: Making Pipe: ',self.pipe_path,'.')
    
    def requestHandler(self):
        ros_ret = 0
        while ros_ret == 0:
            try:
                rclpy.init()
            except:
                a = 1
            self.ros_handler = RobotEnableActionClient()
            self.ros_handler.send_goal(self.goal)
            rclpy.spin(self.ros_handler)
            ros_ret = self.ros_handler._ret
            print('[Get]  MoveJoint result.')
        if ros_ret:
            self.result = 'y' + ' '*19

    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        
        while True:
            try:
                data = os.read(fd, 20)
                if data.decode('utf-8').split(';')[0] == 'RobotEnable':
                    print('[Get]  RobotEnable request.')
                    try:
                        request = data.decode('utf-8')
                        value = request.split(';')[1]
                        self.goal.pin = 2
                        self.goal.value = int(value)
                        
                        self.requestHandler()

                        os.write(fd, self.result.encode('utf-8'))
                        print('[Sent]  RobotEnable result.')
                        time.sleep(self.interval)
                    except:
                        time.sleep(self.interval)

            except:
                print('[Error]  RobotEnable.')
            time.sleep(self.interval/2)


