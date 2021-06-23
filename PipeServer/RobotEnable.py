import os
import time
import threading

import rclpy
from rclpy.executors import ExternalShutdownException,SingleThreadedExecutor
from rclpy.node import Node
from rclpy.action import ActionClient
from driver.action import DrvWriteSdi

class RobotEnableClient(Node):
    def __init__(self):
        super().__init__('RobotEnable')
        self._action_client = ActionClient(self, DrvWriteSdi, 'Driver_Write_Sdi')
        self._ret = 0
        self._count = 0

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
        self._ret = bool(result.sucess)
        self._count += 1


class RobotEnableHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.result = ' '
        self.count = 0
        self.move = 0
        self.executor = SingleThreadedExecutor()
        self.node = RobotEnableClient()
        self.executor.add_node(self.node)
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info]  RobotEnable: Making Pipe: ',self.pipe_path,' exists.')
    
    def rosHandler(self):
        while True:
            try:
                self.executor.spin_once()
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
                data = os.read(fd, 20)
                if data.decode('utf-8').split(';')[0] == 'RobotEnable':
                    print('[Info]  RobotEnable gets request from Pipe.')
                    try:
                        msg = data.decode('utf-8').split(';')[1:-1]
                        
                        goal = DrvWriteSdi.Goal()
                        value = int(msg[0])
                        goal.pin = 2
                        goal.value = value
                                              
                        
                        time1 = time.time()
                        self.node.send_goal(goal)
                        self.count += 1
                        time2 = time.time()
                        print('[Info]  RobotEnable sends request to ROS.')
                        print('[Info]  Node send time',time2-time1)

                        while self.count > self.node._count:
                            #print(self.count,self.node._count)
                            time.sleep(self.interval/2)
                        self.result = self.node._ret
                        time1 = time.time()
                        print('[Info]  RobotEnable gets result from ROS.')
                        print('[Info]  Result:', self.result)
                        print('[Info]  Node spin time',time1-time2)
                        
                        if self.result:
                            self.pipe_result = 'y' + ' '*19

                        os.write(fd,self.pipe_result.encode('utf-8'))
                        print('[Info]  RobotEnable sends result to Pipe.',self.result)
                        self.move += 1
                        print('[Info]  RobotEnable counter',self.move)
                    except:
                        time.sleep(self.interval/2)
                        
                elif data.decode('utf-8')[0] == 'y':
                    print('[Info]  RobotEnable resends result to Pipe.')
                    os.write(fd,data)
                    time.sleep(self.interval)
            except:
                print('[Error]  RobotEnable.')
            time.sleep(self.interval/2)
