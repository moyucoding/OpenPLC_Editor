import threading

import MotionGo
import GetCurJoint
import MoveAbsJoint
import MoveJoint
import MoveLinear
import MoveCircle
import MoveJogJoint
import MoveJogLinear
import MoveJogRotation




def main(interval):

    
    MotionGo_Pipepath = '/tmp/MotionGo.pipe'
    handler_MotionGo = MotionGo.MotionGoHandler(MotionGo_Pipepath)
    thread_MotionGo = threading.Thread(target = handler_MotionGo.runHandler)
    thread_MotionGo.start()

    GetCurJoint_Pipepath = '/tmp/GetCurJoint.pipe'
    handler_GetCurJoint = GetCurJoint.GetCurJointHandler(GetCurJoint_Pipepath, interval)
    thread_GetCurJoint = threading.Thread(target = handler_GetCurJoint.runHandler)
    thread_GetCurJoint.start()

    MoveAbsJoint_Pipepath = '/tmp/MoveAbsJoint.pipe'
    handler_MoveAbsJoint = MoveAbsJoint.MoveAbsJointHandler(MoveAbsJoint_Pipepath, interval)
    thread_MoveAbsJoint = threading.Thread(target = handler_MoveAbsJoint.runHandler)
    thread_MoveAbsJoint.start()

    MoveJoint_Pipepath = '/tmp/MoveJoint.pipe'
    handler_MoveJoint = MoveJoint.MoveJointHandler(MoveJoint_Pipepath, interval)
    thread_MoveJoint = threading.Thread(target = handler_MoveJoint.runHandler)
    thread_MoveJoint.start()

    MoveLinear_Pipepath = '/tmp/MoveLinear.pipe'
    handler_MoveLinear = MoveLinear.MoveLinearHandler(MoveLinear_Pipepath, interval)
    thread_MoveLinear = threading.Thread(target = handler_MoveLinear.runHandler)
    thread_MoveLinear.start()

    MoveCircle_Pipepath = '/tmp/MoveCircle.pipe'
    handler_MoveCircle = MoveCircle.MoveCircleHandler(MoveCircle_Pipepath, interval)
    thread_MoveCircle = threading.Thread(target = handler_MoveCircle.runHandler)
    thread_MoveCircle.start()

    MoveJogJoint_Pipepath = '/tmp/MoveJogJoint.pipe'
    handler_MoveJogJoint = MoveJogJoint.MoveJogJointHandler(MoveJogJoint_Pipepath, interval)
    thread_MoveJogJoint = threading.Thread(target = handler_MoveJogJoint.runHandler)
    thread_MoveJogJoint.start()

    MoveJogLinear_Pipepath = '/tmp/MoveJogLinear.pipe'
    handler_MoveJogLinear = MoveJogLinear.MoveJogLinearHandler(MoveJogLinear_Pipepath, interval)
    thread_MoveJogLinear = threading.Thread(target = handler_MoveJogLinear.runHandler)
    thread_MoveJogLinear.start()

    MoveJogRotation_Pipepath = '/tmp/MoveJogRotation.pipe'
    handler_MoveJogRotation = MoveJogRotation.MoveJogRotationHandler(MoveJogRotation_Pipepath, interval)
    thread_MoveJogRotation = threading.Thread(target = handler_MoveJogRotation.runHandler)
    thread_MoveJogRotation.start()
    

    



if __name__ == '__main__':
    interval = 0.02
    main(interval)
