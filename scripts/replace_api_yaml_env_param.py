import yaml
import glob
import os
import Audit_res, utils

FILE_NAME = "replace_api_yaml_env_param.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

environment_config = utils.get_env_config(os.environ["CONFIG_FILES_DIR"])

print(environment_config)

def replace_api_env_params(target_dir):
    yamlFiles=glob.glob(target_dir + "/*.yaml")

    for ymlFile in yamlFiles:
        print(INFO + "Replacing placeholders in file: " + ymlFile.replace(WORKING_DIR_BASIC + "/","") + "...")
        with open(target_dir + "/" + ymlFile,'r') as f:
            data = f.read()
            dataMap = yaml.safe_load(data)

        if "basePath" in dataMap:
            data = data.replace("PROVORG",os.environ["PROV_ORG_NAME"])
            data = data.replace("CATALOGNAME",os.environ["PROV_ORG_CATALOG_NAME"])
            data = data.replace("APIGWYBASEURL",environment_config["APIC_GATEWAY_URL"] + "/" + os.environ["PROV_ORG_NAME"] + "/" + os.environ["PROV_ORG_CATALOG_NAME"])
            # print("modified data : ",data)
            with open(target_dir + "/" + ymlFile,"w") as f:
                f.write(data)


def orchestrate():
    try:
        replace_api_env_params(WORKING_DIR_BASIC)
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Replace_placeholders", "SUCCESS")
        print(INFO + "Replace_placeholders SUCCESS")

    except Exception as e:
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Replace_placeholders", "FAILED")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))



orchestrate()
