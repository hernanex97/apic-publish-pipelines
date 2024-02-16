import os
import Audit_res

FILE_NAME = "initialize_apic_deploy.py"
INFO = "["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

def create_workspace_dir():
    try:
        currentDirectory = os.getcwd()
        print(INFO + "Current directory: ", currentDirectory)

        # create a build directory
        print(INFO + "Workspace: ", WORKING_DIR_BASIC)
        if not os.path.isdir(WORKING_DIR_BASIC):
            os.makedirs(WORKING_DIR_BASIC)
    except Exception as e:
         raise Exception("in " + FILE_NAME + " create_workspace_dir() : FAILED : " + repr(e))

def init():
    try:
        create_workspace_dir()
        print(INFO + "Initialize_APIC_Deploy SUCESS")
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Initialize_APIC_Deploy", "SUCCESS")
    except Exception as e:
        print("[ERROR] - Exception in  " + FILE_NAME + " type(e) : ", repr(e))
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Initialize_APIC_Deploy", "FAILED : " + repr(e))
        raise Exception("[ERROR] - In " + FILE_NAME + ": FAILED : " + repr(e))

init()