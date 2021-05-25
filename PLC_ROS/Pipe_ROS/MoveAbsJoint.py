import os
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from motion.action import MotionMoveAbsJoint

class MoveAbsJointActionClient(Node):

    def __init__(self):
        super().__init__('MotionMoveAbsJoint')
        
        self._action_client = ActionClient(self, MotionMoveAbsJoint, 'Motion/MoveAbsJoint')
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




class MoveAbsJointHandler():
    def __init__(self, path) -> None:
        super().__init__()
        self.pipe_path = path

        try:
            os.mkfifo(self.pipe_path)
        except OSError:
            print('[Error]  MoveAbsJoint: Making Pipe: ',self.pipe_path,'.')
    
    def runHandler(self):
        fd = os.open(self.pipe_path, os.O_CREAT | os.O_RDWR)
        while True:
            try:
                data = os.read(fd, 400)
                if data.decode('utf-8').split(';')[0] == 'MoveAbsJoint':
                    print('[Get]  MoveAbsJoint request.')
                    try:
                        request = data.decode('utf-8')
                        msg = request.split(';')[1:-1]
                        #Create a goal
                        goal = MotionMoveAbsJoint.Goal()
                        goal.id = 1
                        joint = [float(x) for x in msg[0].split(',')[:]]
                        goal.joint = [0.0] * 8
                        for i in range(len(joint)):
                            goal.joint[i] = joint[i]

                        extjoint = [float(x) for x in msg[1].split(',')[:]]
                        goal.extjoint = [0.0] * 8
                        for i in range(len(extjoint)):
                            goal.extjoint[i] = extjoint[i]

                        load = [float(x) for x in msg[2].split(',')[:]]
                        goal.joint = [0.0] * 10
                        for i in range(len(load)):
                            goal.load[i] = load[i]

                        goal.speed = float(msg[3])
                        goal.zone = float(msg[4])
                        
                        rclpy.init()
                        self.ros_handler = MoveAbsJointActionClient()
                        self.ros_handler.send_goal(goal)
                        rclpy.spin(self.ros_handler)
                        
                        print('[Get]  MoveAbsJoint result.')
                        print('[Sent]  MoveAbsJoint result.')
                        if self.ros_handler._ret:
                            validcode = 'y' + ' '*9
                            os.write(fd,validcode.encode('utf-8'))
                        else:
                            errorcode = 'n1'+' '*8
                            os.write(fd,errorcode.encode('utf-8'))
                    except:
                        errorcode = 'n1'+' '*8
                        os.write(fd,errorcode.encode('utf-8'))
            except:
                print('[Error]  MoveAbsJoint')
            time.sleep(0.1)