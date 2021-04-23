import os
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ros_motion.action import MotionMoveAbsJoint

class MoveAbsJointActionClient(Node):

    def __init__(self):
        super().__init__('motionmoveabsjoint_action_client')
        
        self._action_client = ActionClient(self, MotionMoveAbsJoint, 'motionmoveabsjoint')
        self._action_result = 0

    def send_goal(self, goal_msg):
        # goal_msg = MotionMoveAbsJoint.Goal()

        # goal_msg.id = 1
        # goal_msg.joint = [1.1,2.2,3.3,4.4,5.5,6.6]
        # goal_msg.extjoint = [0.0,0.0,0.0,0.0,0.0,0.0]
        # goal_msg.load = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        # goal_msg.speed = 0.5
        # goal_msg.zone = 0.5

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
        self.get_logger().info('Get Result :(')
        self.get_logger().info('Result: {0}'.format(result.ret))
        self._action_result = int(result.ret)
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.cnt))




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
                data = os.read(fd, 500)
                if data.decode('utf-8')!='y0' :
                    print('[Get]  MoveAbsJoint request.')
                    #print(data.decode('utf-8'))
                    request = data.decode('utf-8')
                    #goal = int(float(request.split(',')[1])//1)
                    print('[Request]: ',request)
                    #
                    # Do Something
                    # 

                    #Create a goal
                    request_msg = request.split(',')
                    goal = MotionMoveAbsJoint.Goal()
                    goal.id = 1
                    goal.joint = [float(x) for x in request_msg[1:7]]
                    goal.extjoint = [float(x) for x in request_msg[7:13]]
                    goal.load = [float(x) for x in request_msg[13:23]]
                    goal.speed = float(request_msg[23])
                    goal.zone = float(request_msg[24])
                    
                    rclpy.init()
                    self.ros_handler = MoveAbsJointActionClient()
                    self.ros_handler.send_goal(goal)
                    rclpy.spin(self.ros_handler)
                    
                    print('[Get]  MoveAbsJoint result.')
                    print('[Sent]  MoveAbsJoint result.')
                    if self.ros_handler._action_result:
                        os.write(fd,'yf0'.encode('utf-8'))
                    else:
                        os.write(fd,'ny1'.encode('utf-8'))
            except:
                print('[Error]  MoveAbsJoint')
            time.sleep(0.1)