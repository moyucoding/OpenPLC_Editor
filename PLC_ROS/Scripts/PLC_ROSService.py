import threading

import MotionGo
import MoveAbsJoint
import GetCurJoint


def main():

    
    MotionGo_Pipepath = '/tmp/MotionGo.pipe'
    handler_MotionGo = MotionGo.MotionGoHandler(MotionGo_Pipepath)
    thread_MotionGo = threading.Thread(target = handler_MotionGo.runHandler)
    thread_MotionGo.start()

    MoveAbsJoint_Pipepath = '/tmp/MoveAbsJoint.pipe'
    handler_MoveAbsJoint = MoveAbsJoint.MoveAbsJointHandler(MoveAbsJoint_Pipepath)
    thread_MoveAbsJoint = threading.Thread(target = handler_MoveAbsJoint.runHandler)
    thread_MoveAbsJoint.start()

    GetCurJoint_Pipepath = '/tmp/GetCurJoint.pipe'
    handler_GetCurJoint = GetCurJoint.GetCurJointHandler(GetCurJoint_Pipepath)
    thread_GetCurJoint = threading.Thread(target = handler_GetCurJoint.runHandler)
    thread_GetCurJoint.start()



if __name__ == '__main__':
    main()
