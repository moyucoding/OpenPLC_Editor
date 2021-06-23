import threading

import rclpy

import GetCurJoint
import GetCurState
import MotionGo
import MoveAbsJoint
import MoveCircle
import MoveJogJoint
import MoveJogLinear
import MoveJogRotation
import MoveJoint
import MoveLinear
import RobotEnable

class ServiceHandler():
    def __init__(self):
        self.interval = 0.02

        self.GetCurJoint_Pipepath = '/tmp/GetCurJoint.pipe'
        self.GetCurState_Pipepath = '/tmp/GetCurState.pipe'
        self.MotionGo_Pipepath = '/tmp/MotionGo.pipe'
        self.MoveAbsJoint_Pipepath = '/tmp/MoveAbsJoint.pipe'
        self.MoveCircle_Pipepath = '/tmp/MoveCircle.pipe'
        self.MoveJogJoint_Pipepath = '/tmp/MoveJogJoint.pipe'
        self.MoveJogLinear_Pipepath = '/tmp/MoveJogLinear.pipe'
        self.MoveJogRotation_Pipepath = '/tmp/MoveJogRotation.pipe'
        self.MoveJoint_Pipepath = '/tmp/MoveJoint.pipe'
        self.MoveLinear_Pipepath = '/tmp/MoveLinear.pipe'
        self.RobotEnable_Pipepath = '/tmp/RobotEnable.pipe'
    
    def run(self, interval):
        self.interval = interval
        
        handler_GetCurJoint = GetCurJoint.GetCurJointHandler(self.GetCurJoint_Pipepath, self.interval)
        thread_GetCurJoint = threading.Thread(target=handler_GetCurJoint.run)
        thread_GetCurJoint.start()

        handler_GetCurState = GetCurState.GetCurStateHandler(self.GetCurState_Pipepath, self.interval)
        thread_GetCurState = threading.Thread(target=handler_GetCurState.run)
        thread_GetCurState.start()

        handler_MotionGo = MotionGo.MotionGoHandler(self.MotionGo_Pipepath, self.interval)
        thread_MotionGo = threading.Thread(target=handler_MotionGo.run)
        thread_MotionGo.start()

        handler_MoveAbsJoint = MoveAbsJoint.MoveAbsJointHandler(self.MoveAbsJoint_Pipepath, self.interval)
        thread_MoveAbsJoint = threading.Thread(target=handler_MoveAbsJoint.run)
        thread_MoveAbsJoint.start()

        handler_MoveCircle = MoveCircle.MoveCircleHandler(self.MoveCircle_Pipepath, self.interval)
        thread_MoveCircle = threading.Thread(target=handler_MoveCircle.run)
        thread_MoveCircle.start()

        handler_MoveJogJoint = MoveJogJoint.MoveJogJointHandler(self.MoveJogJoint_Pipepath, self.interval)
        thread_MoveJogJoint = threading.Thread(target=handler_MoveJogJoint.run)
        thread_MoveJogJoint.start()
        
        handler_MoveJogLinear = MoveJogLinear.MoveJogLinearHandler(self.MoveJogLinear_Pipepath, self.interval)
        thread_MoveJogLinear = threading.Thread(target=handler_MoveJogLinear.run)
        thread_MoveJogLinear.start()

        handler_MoveJogRotation = MoveJogRotation.MoveJogRotationHandler(self.MoveJogRotation_Pipepath, self.interval)
        thread_MoveJogRotation = threading.Thread(target=handler_MoveJogRotation.run)
        thread_MoveJogRotation.start()

        handler_MoveJoint = MoveJoint.MoveJointHandler(self.MoveJoint_Pipepath, self.interval)
        thread_MoveJoint = threading.Thread(target=handler_MoveJoint.run)
        thread_MoveJoint.start()

        handler_MoveLinear = MoveLinear.MoveLinearHandler(self.MoveLinear_Pipepath, self.interval)
        thread_MoveLinear = threading.Thread(target=handler_MoveLinear.run)
        thread_MoveLinear.start()

        handler_RobotEnable = RobotEnable.RobotEnableHandler(self.RobotEnable_Pipepath, self.interval)
        thread_RobotEnable = threading.Thread(target=handler_RobotEnable.run)
        thread_RobotEnable.start()
if __name__ == '__main__':
    plc_interval = 0.015
    try:
        rclpy.init()
        pipe_server = ServiceHandler()
        pipe_server.run(plc_interval)
    except:
        rclpy.shutdown()
