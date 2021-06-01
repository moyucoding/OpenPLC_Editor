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
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)

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
        #self.get_logger().info('Get Result :(')
        self.get_logger().info('Result: {0}'.format(result.ret))
        self._ret = int(result.ret)
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        #self.get_logger().info('Received feedback: {0}'.format(feedback.cnt))




class MoveJointHandler():
    def __init__(self, path, interval) -> None:
        super().__init__()
        self.pipe_path = path
        self.interval = interval
        self.ret = ' '

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveJoint: Making Pipe: ',self.pipe_path,'.')
    
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
                        
                        rclpy.init()
                        self.ros_handler = MoveJointActionClient()
                        self.ros_handler.send_goal(goal)
                        rclpy.spin(self.ros_handler)
                        
                        print('[Get]  MoveJoint result.')
                        print('[Sent]  MoveJoint result.')
                        if self.ros_handler._ret:
                            self.ret = 'y' + ' '*399
                        else:
                            self.ret = 'n1'+' '*398
                        os.write(fd,self.ret.encode('utf-8'))
                        time.sleep(self.interval)
                    except:
                        self.ret = 'n1'+' '*398
                        os.write(fd,self.encode('utf-8'))
                        time.sleep(self.interval)
            except:
                print('[Error]  MoveJoint')
            time.sleep(self.interval/2)