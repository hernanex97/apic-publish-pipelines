import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import parse_api_yaml_get_basepath
import Audit_res, utils


FILE_NAME = "test_apic_apis.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

environment_config = utils.get_env_config(os.environ["CONFIG_FILES_DIR"])

def test_apis(var_api_basepath_list, apic_gwy_base_url): 
    var_final_result = {}
    for apiname, basepath in var_api_basepath_list.items():
        # print("apiname:", apiname)
        # print("basepath : ", basepath)
        url = "https://" + apic_gwy_base_url + basepath + "/stub"

        # print("url : ", url)
        reqheaders = {
            "Content-Type" : "application/json",
            "Accept" : "application/json"
        }
        """
        response = requests.get(url, headers=reqheaders, verify=False, timeout=10)
        """
        resp_statuscode = None
        
        try :
            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
            s.mount(apic_gwy_base_url, HTTPAdapter(max_retries=retries))
    
            #resi = ResilientSession()
            response = s.get(url, headers=reqheaders, verify=False, timeout=10)
            resp_statuscode = response.status_code
        except Exception as e:
            # print("test_apis() SOME EXCEPTION OCCURRED during testing: ",e)
            resp_statuscode = e
        
        var_final_result[apiname] = resp_statuscode

    return var_final_result

def orchestrate():
    try:
        var_api_basepath_dict = parse_api_yaml_get_basepath.get_basepath_from_api(WORKING_DIR_BASIC)
        print(INFO + "APIs to test:",var_api_basepath_dict)
        var_final_api_test_result_dict = test_apis(var_api_basepath_dict,
                                                    environment_config["APIC_GATEWAY_URL"] + "/" + \
                                                    os.environ["PROV_ORG_TITLE"].strip().replace(" ","-").lower() + "/" + \
                                                    os.environ["PROV_ORG_CATALOG_NAME"])
        
        print(INFO + "api_test_audit:",var_final_api_test_result_dict)
        Audit_res.update_test_apis_audit(WORKING_DIR_BASIC, var_final_api_test_result_dict)
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "APIC_API_Test", "SUCCESS")
        print(INFO + "APIC_API_Test SUCCESS")
    except Exception as e:
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "APIC_API_Test", "FAILED")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))

orchestrate()
