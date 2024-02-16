import json

AUDIT_FILENAME = "apic-pipeline-audit.json"
FILE_NAME = "print_audit.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

def orchestrate():
    try:
      with open(WORKING_DIR_BASIC + "/" + AUDIT_FILENAME,'r') as f:
        data = f.read()
        data_json = json.loads(data)
        print(INFO + "AUDIT")
        print(INFO + "-----")
        print(json.dumps(data_json, indent=4, sort_keys=False))

    except Exception as e:
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))

orchestrate()
