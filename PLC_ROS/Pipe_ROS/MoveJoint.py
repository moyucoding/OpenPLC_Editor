import os
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionMoveJoint

class MoveJointActionClient(Node):

    def __init__(self):
        super().__init__('MotionMoveJoint')
        self._action_client = ActionClient(self, MotionMoveJoint, 'Motion/MoveJoint')
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
        self._ret = int(result.ret)
        rclpy.shutdown()


class MoveJointHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.result = ' '

        self.goal = MotionMoveJoint.Goal()
        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJoint: Making Pipe: ',self.pipe_path,'.')
    
    def requestHandler(self):
        ros_ret = 0
        while ros_ret == 0:
            try:
                rclpy.init()
            except:
                a = 1
            self.ros_handler = MoveJointActionClient()
            self.ros_handler.send_goal(self.goal)
            rclpy.spin(self.ros_handler)
            ros_ret = self.ros_handler._ret
            print('[Get]  MoveJoint result.')
        if ros_ret:
            self.result = 'y' + ' '*399
        else:
            self.result = 'n1'+' '*398

    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveJoint':
                    print('[Get]  MoveJoint request.')
                    try:
                        request = data.decode('utf-8')
                        msg = request.split(';')[1:-1]
                        #Create a goal
                        self.goal = MotionMoveJoint.Goal()
                        self.goal.id = 1
                        self.goal.user = [1.0] + [0.0] * 6
                        self.goal.tool = [0.0] * 7
                        self.goal.topoint = [float(x) for x in msg[0].split(',')[:]]

                        extjoint = [float(x) for x in msg[1].split(',')[:]]
                        self.goal.extjoint = [0.0] * 8
                        for i in range(len(extjoint)):
                            self.goal.extjoint[i] = extjoint[i]

                        load = [float(x) for x in msg[2].split(',')[:]]
                        self.goal.load = [0.0] * 10
                        for i in range(len(load)):
                            self.goal.load[i] = load[i]

                        self.goal.speed = float(msg[3])
                        self.goal.zone = float(msg[4])
                        
                        self.requestHandler()

                        os.write(fd,self.result.encode('utf-8'))
                        print('[Sent]  MoveJoint result.')
                        time.sleep(self.interval)
                    except:
                        time.sleep(self.interval)
                        
            except:
                print('[Error]  MoveJoint.')
            time.sleep(self.interval/2)