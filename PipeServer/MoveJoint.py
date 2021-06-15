import os
import time
import threading

import rclpy
from rclpy.executors import ExternalShutdownException,SingleThreadedExecutor
from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionMoveJoint

class MoveJointClient(Node):
    def __init__(self):
        super().__init__('MotionMoveJoint')
        self._action_client = ActionClient(self, MotionMoveJoint, 'Motion/MoveJoint')
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


class MoveJointHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.result = ' '
        self.count = 0

        self.executor = SingleThreadedExecutor()
        self.node = MoveJointClient()
        self.executor.add_node(self.node)
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Info]  MoveJoint: Making Pipe: ',self.pipe_path,' exists.')
    
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
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveJoint':
                    print('[Info]  MoveJoint gets request from Pipe.')
                    try:
                        msg = data.decode('utf-8').split(';')[1:-1]
                        
                        goal = MotionMoveJoint.Goal()
                        goal.id = 1
                        goal.user = [1.0] + [0.0] * 6
                        goal.tool = [0.0] * 7
                        goal.topoint = [float(x) for x in msg[0].split(',')[:]]

                        extjoint = [float(x) for x in msg[1].split(',')[:]]
                        goal.extjoint = [0.0] * 8
                        for i in range(len(extjoint)):
                            goal.extjoint[i] = extjoint[i]

                        load = [float(x) for x in msg[2].split(',')[:]]
                        goal.load = [0.0] * 10
                        for i in range(len(load)):
                            goal.load[i] = load[i]

                        goal.speed = float(msg[3])
                        goal.zone = float(msg[4])

                        time1 = time.time()
                        self.node.send_goal(goal)
                        self.count += 1
                        time2 = time.time()
                        print('[Info]  MoveJoint sends request to ROS.')
                        print('[Info]  Goal:', goal.topoint)
                        print('[Info]  Node send time',time2-time1)

                        while self.count != self.node._count:
                            time.sleep(self.interval/2)
                        self.result = self.node._ret
                        time1 = time.time()
                        print('[Info]  MoveJoint gets result from ROS.')
                        print('[Info]  Result:', self.result)
                        print('[Info]  Node spin time',time1-time2)

                        if self.result > 0:
                            self.pipe_result = 'y' + ' '*399
                        elif self.result == 0:
                            time1 = time.time()
                            print('[Info]  MoveJoint resends request from ROS.')
                            while self.node._ret <= 0:
                                time.sleep(self.interval/2)
                                self.node.send_goal(goal)
                                self.count += 1
                                while self.count != self.node._count:
                                    time.sleep(self.interval)
                            time2 = time.time()
                            print('[Info]  Node resend time',time2-time1)
                            self.result = self.node._ret
                            self.pipe_result = 'y' + ' '*399
                        else:
                            self.pipe_result = 'n1'+' '*398
                        
                        os.write(fd,self.pipe_result.encode('utf-8'))
                        print('[Info]  MoveJoint sends result to Pipe.',self.result)
                        
                    except:
                        time.sleep(self.interval/2)

                elif data.decode('utf-8')[0] == 'y' or data.decode('utf-8')[0] == 'n':
                    print('[Info]  MoveJoint resends result to Pipe.')
                    os.write(fd,data)
                    time.sleep(self.interval)
            except:
                print('[Error]  MoveJoint.')
            time.sleep(self.interval/2)
