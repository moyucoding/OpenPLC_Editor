import os
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from driver.action import DriverWriteSdi

class RobotEnableClient(Node):
    def __init__(self):
        super().__init__('RobotEnable')
        self._action_client = ActionClient(self, DriverWriteSdi, 'Driver/Driver_Write_Sdi')
        self._ret = 0
    
    def send_goal(self, goal_msg):
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            return

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.result = int(result.ret)
        rclpy.shutdown()
        

class RobotEnableHandler():
    def __init__(self, path, interval):
        super().__init__()
        self.pipe_path = path
        self.interval = interval

        self.node = RobotEnableClient()
        self.goal = DriverWriteSdi.Goal()
        self.result = ''


        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info] RobotEnable: Pipe: ',self.pipe_path,' exists.')
    
    def rosHandler(self):
        ros_ret = 0
        while ros_ret == 0:
            self.node.send_goal(self.goal)
            print('[Info]  RobotEnable sends request to ROS.')
            rclpy.spin(self.node)
            try:
                rclpy.init()
            except:
                a = 1
            ros_ret = self.node._ret
        print('[Info]  RobotEnable gets result from ROS.')
        if ros_ret:
            self.result = 'y' + ' '*19

    def run(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                pipe_raw = os.read(fd, 20)
                if pipe_raw.decode('utf-8').split(';')[0] == 'RobotEnable':
                    print('[Info]  RobotEnable gets request from Pipe.')
                    try:
                        pipe_msg = pipe_raw.decode('utf-8').split(';')[1:-1]
                        
                        self.goal = DriverWriteSdi.Goal()
                        self.goal.pin = 2
                        self.goal.value = int(pipe_msg[0])
                    
                        self.rosHandler()

                        os.write(fd,self.result.encode('utf-8'))
                        print('[Info]  RobotEnable sends result to Pipe.')
                        time.sleep(self.interval)
                    except:
                        time.sleep(self.interval)
            except:
                print('[Error] RobotEnable.')
            time.sleep(self.interval/2)