import os
import json

FILE_NAME = "Audit_res.py"
AUDIT_FILENAME = "apic-pipeline-audit.json"

def write_to_file(ENV_LOCAL_TARGET_DIR, fileContent):
    with open(ENV_LOCAL_TARGET_DIR + "/" + AUDIT_FILENAME,"w+") as f:
        f.write(json.dumps(fileContent))

def readfile_myAudit(ENV_LOCAL_TARGET_DIR):
    myAudit = None
    if os.path.isfile(ENV_LOCAL_TARGET_DIR + "/" + AUDIT_FILENAME):
        with open(ENV_LOCAL_TARGET_DIR + "/" + AUDIT_FILENAME) as f:
            myAudit = json.load(f)
    else:
        myAudit = {}
    return myAudit

def update_stage_res(ENV_LOCAL_TARGET_DIR, stage_name, stage_res):
    myAudit = readfile_myAudit(ENV_LOCAL_TARGET_DIR)

    if "STAGE_SUMMARY" in myAudit.keys():
        if stage_name in myAudit["STAGE_SUMMARY"]:
            myAudit["STAGE_SUMMARY"][stage_name]["Result"] = stage_res
        else:
            temp = {"Result" : stage_res}
            myAudit["STAGE_SUMMARY"][stage_name] = temp
    else:
        temp = {stage_name : {"Result" : stage_res}}
        myAudit["STAGE_SUMMARY"] = temp
    
    write_to_file(ENV_LOCAL_TARGET_DIR, myAudit)

def update_product_download_audit(ENV_LOCAL_TARGET_DIR, product_download_audit):
    myAudit = readfile_myAudit(ENV_LOCAL_TARGET_DIR)
    for key,value in product_download_audit.items():
        dyfg = {"Download_Yaml_From_Git" : value}
        if "Products" in myAudit.keys():
            if key in myAudit["Products"]:
                myAudit["Products"][key]["Download_Yaml_From_Git"] = value
            else:
                myAudit["Products"][key] = dyfg
        else:
            myAudit["Products"] = {key: dyfg}

    write_to_file(ENV_LOCAL_TARGET_DIR, myAudit)

def update_api_download_audit(ENV_LOCAL_TARGET_DIR, api_download_audit):
    myAudit = readfile_myAudit(ENV_LOCAL_TARGET_DIR)
    for key,value in api_download_audit.items():
        dyfg = {"Download_Yaml_From_Git" : value}
        if "APIs" in myAudit.keys():
            if key in myAudit["APIs"]:
                myAudit["APIs"][key]["Download_Yaml_From_Git"] = value
            else:
                myAudit["APIs"][key] = dyfg
        else:
            myAudit["APIs"] = {key: dyfg}

    write_to_file(ENV_LOCAL_TARGET_DIR, myAudit)

def update_apic_publish_audit(ENV_LOCAL_TARGET_DIR, apic_publish_audit):
    myAudit = readfile_myAudit(ENV_LOCAL_TARGET_DIR)
    for key,value in apic_publish_audit.items():
        key = key.replace(".yaml", "")
        temp = {"Publish" : value}
        if "Products" in myAudit.keys():
            if key in myAudit["Products"]:
                myAudit["Products"][key]["Publish"] = value
            else:
                myAudit["Products"][key] = temp
        else:
            myAudit["Products"] = {key: temp}

    write_to_file(ENV_LOCAL_TARGET_DIR, myAudit)

def update_test_apis_audit(ENV_LOCAL_TARGET_DIR, test_apis_audit):
    myAudit = readfile_myAudit(ENV_LOCAL_TARGET_DIR)

    for key,value in test_apis_audit.items():
        temp = {"Test_Result" : value}
        if "APIs" in myAudit.keys():
            if key in myAudit["APIs"]:
                myAudit["APIs"][key]["Test_Result"] = value
            else:
                myAudit["APIs"][key] = temp
        else:
            myAudit["APIs"] = {key: temp}

    write_to_file(ENV_LOCAL_TARGET_DIR, myAudit)
