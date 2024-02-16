import os
import json
import parse_apic_product_yaml_get_api_names
import raw_file_download_from_git
import Audit_res

FILE_NAME = "download_api_files_from_git.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

def download_api_yaml():
    try:
        var_product_tuple = raw_file_download_from_git.get_all_file_names_from_git_enterprise(os.environ["GIT_PRODUCTS_APIS_URL"],
                                                                                            os.environ["GIT_PRODUCTS_APIS_BRANCH"],
                                                                                            os.environ["GIT_PRIV_TOKEN"],
                                                                                            os.environ['GIT_PRODUCTS_PATH'])

        print(INFO + "Products to inspect for APIs:", var_product_tuple)
        api_list = parse_apic_product_yaml_get_api_names.get_api_list_from_product(WORKING_DIR_BASIC, var_product_tuple)

        # print("API LIST", api_list)

        api_download_audit = {}

        for api_file_name in api_list:
            print(INFO + "Downloading file: " + api_file_name + "...")
            api_file_name = api_file_name.replace(".yaml", "")
            download_file_from_git_res = raw_file_download_from_git.download_file_from_git_enterprise(os.environ["GIT_PRODUCTS_APIS_URL"],
                                                                                                    os.environ["GIT_PRODUCTS_APIS_BRANCH"],
                                                                                                    os.environ["GIT_PRIV_TOKEN"],
                                                                                                    os.environ['GIT_APIS_PATH'],
                                                                                                    api_file_name,
                                                                                                    WORKING_DIR_BASIC)
            if download_file_from_git_res["returncode"] == "200":
                api_download_audit[api_file_name] = "SUCCESS"
            else:
                if "404: Not Found" in download_file_from_git_res["stderr"]:
                    api_download_audit[api_file_name] = "FAILED - 404 File Not Found"
                else:
                    api_download_audit[api_file_name] = "FAILED"

        print(INFO + "api_download_audit: ",api_download_audit)
        Audit_res.update_api_download_audit(WORKING_DIR_BASIC, api_download_audit)

        isSuccess = True
        for key, value in api_download_audit.items():
            if "FAILED" in value:
                isSuccess = False

        if isSuccess == True:
            Audit_res.update_stage_res(WORKING_DIR_BASIC, "API_Download", "SUCCESS")
            print(INFO + "API_Download SUCCESS")
        else:
            raise Exception("An error occurred downloading an API file")
    except Exception as e:
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "API_Download", "FAILED")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))

download_api_yaml()
