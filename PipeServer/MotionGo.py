import os
import time
import threading

import rclpy
from rclpy.executors import ExternalShutdownException,SingleThreadedExecutor
from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionGo

class MotionGoClient(Node):
    def __init__(self):
        super().__init__('MotionGo')
        self._action_client = ActionClient(self, MotionGo, 'Motion/Go')
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
        self._ret = int(result.ret)
        self._count += 1


class MotionGoHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.result = ' '
        self.count = 0
        self.move = 0
        self.executor = SingleThreadedExecutor()
        self.node = MotionGoClient()
        self.executor.add_node(self.node)
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info]  MotionGo: Making Pipe: ',self.pipe_path,' exists.')
    
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
                data = os.read(fd, 10)
                if data.decode('utf-8').split(';')[0] == 'MotionGo':
                    print('[Info]  MotionGo gets request from Pipe.')
                    try:                        
                        goal = MotionGo.Goal()                                              
                        
                        time1 = time.time()
                        self.node.send_goal(goal)
                        self.count += 1
                        time2 = time.time()
                        print('[Info]  MotionGo sends request to ROS.')
                        print('[Info]  Node send time',time2-time1)

                        while self.count > self.node._count:
                            #print(self.count,self.node._count)
                            time.sleep(self.interval/2)
                        self.result = self.node._ret
                        time1 = time.time()
                        print('[Info]  MotionGo gets result from ROS.')
                        print('[Info]  Result:', self.result)
                        print('[Info]  Node spin time',time1-time2)
                        
                        if self.result:
                            self.pipe_result = 'y' + ' '*9

                        os.write(fd,self.pipe_result.encode('utf-8'))
                        print('[Info]  MotionGo sends result to Pipe.',self.result)
                        self.move += 1
                        print('[Info]  MotionGo counter',self.move)
                    except:
                        time.sleep(self.interval/2)
                        
                elif data.decode('utf-8')[0] == 'y':
                    print('[Info]  MotionGo resends result to Pipe.')
                    os.write(fd,data)
                    time.sleep(self.interval)
            except:
                print('[Error]  MotionGo.')
            time.sleep(self.interval/2)
