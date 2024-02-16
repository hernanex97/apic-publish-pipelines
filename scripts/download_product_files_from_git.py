import os
import raw_file_download_from_git
import Audit_res

FILE_NAME = "download_product_files_from_git.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"

def product_files_from_git():
    try:
        var_product_tuple = raw_file_download_from_git.get_all_file_names_from_git_enterprise(os.environ["GIT_PRODUCTS_APIS_URL"],
                                                                                            os.environ["GIT_PRODUCTS_APIS_BRANCH"],
                                                                                            os.environ["GIT_PRIV_TOKEN"],
                                                                                            os.environ['GIT_PRODUCTS_PATH'])

        print(INFO + "Product files to be downloaded:", var_product_tuple)
        product_download_audit = {}

        for filename_to_download in var_product_tuple:
            print(INFO + "Downloading file: " + filename_to_download + "...")
            download_file_from_git_res = raw_file_download_from_git.download_file_from_git_enterprise(os.environ["GIT_PRODUCTS_APIS_URL"],
                                                                                        os.environ["GIT_PRODUCTS_APIS_BRANCH"],
                                                                                        os.environ["GIT_PRIV_TOKEN"],
                                                                                        os.environ["GIT_PRODUCTS_PATH"],
                                                                                        filename_to_download,
                                                                                        WORKING_DIR_BASIC)
            if download_file_from_git_res["returncode"] == "200":
                product_download_audit[filename_to_download] = "SUCCESS"
            else:
                if "404: Not Found" in download_file_from_git_res["stderr"]:
                    product_download_audit[filename_to_download] = "FAILED - 404 File Not Found"
                else:
                    product_download_audit[filename_to_download] = "FAILED"

        print(INFO + "Product_download_audit: ",product_download_audit)
        Audit_res.update_product_download_audit(WORKING_DIR_BASIC, product_download_audit)

        isSuccess = True
        for key,value in product_download_audit.items():
            if "FAILED" in value:
                isSuccess = False

        if isSuccess == True:
            Audit_res.update_stage_res(WORKING_DIR_BASIC, "Product_Download", "SUCCESS")
            print(INFO + "Product_Download SUCCESS")
        else:
            raise Exception("An error ocurred downloading a Product file")
    except Exception as e:
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Product_Download", "FAILED")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))


product_files_from_git()