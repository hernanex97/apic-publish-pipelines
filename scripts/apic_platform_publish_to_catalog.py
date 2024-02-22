import os
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import json
import yaml
import apic_platform_get_bearer_token
import raw_file_download_from_git
import Audit_res
import utils

FILE_NAME = "apic_platform_publish_to_catalog.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 
WORKING_DIR_BASIC = "../WORKSPACE"


def get_api_refs_from_product(env_local_target_dir, product_file_name):
    var_apilist = []
    try:
        with open(f"{env_local_target_dir}/{product_file_name}", "r") as f:
            data = yaml.safe_load(f)
        
        # Check if the 'apis' key is present in the data
        if "apis" in data:
            for api_name, api_info in data["apis"].items():
                # Check if '$ref' is in the current api_info dictionary
                if "$ref" in api_info:
                    # Extract the value of '$ref' and append it to var_apilist
                    var_apilist.append(api_info["$ref"])
    except Exception as e:
        print("[ERROR] Exception trying to open the file")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))
    return var_apilist

def delete_all_products(apic_platform_base_url, apic_mgmt_provorg, apic_mgmt_catalog, var_bearer_token): 
    try:

        url = "https://" + apic_platform_base_url + "/catalogs/" + apic_mgmt_provorg + "/" + apic_mgmt_catalog + "/products?confirm=" + apic_mgmt_catalog
                
        print(INFO + "Deleting all existing products in org: " + apic_mgmt_provorg + " and catalog: " + apic_mgmt_catalog)

        reqheaders = {
            "Accept" : "application/json",
            "Authorization" : "Bearer " + var_bearer_token
        }

        s = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
        s.mount(url, HTTPAdapter(max_retries=retries))

        response = s.delete(url, headers=reqheaders, verify=False, timeout=300)
        print(INFO + "Response status_code:",response.status_code)
        if "204" not in str(response.status_code):
            raise Exception("An error occurred deleting all products")

    except Exception as e:
        raise Exception("An exception occurred deleting all products")

def publish_to_catalog_using_platform_api(apic_platform_base_url, apic_mgmt_provorg, apic_mgmt_catalog, env_local_target_dir, product_file_name, var_bearer_token): 
    resp_json = {}
    try:
        url = "https://" + apic_platform_base_url + "/catalogs/" + apic_mgmt_provorg + "/" + apic_mgmt_catalog + "/publish?migrate_subscriptions=true"
        print("url for publish")
        print(url)
        """ for single product with single api
        multipart_data = MultipartEncoder(
            fields={
                # a file upload field below syntax works
                #'product': ('payment_1.0.0.yaml', open('./temp-ws/BUILD-WS-3/payment_1.0.0.yaml', 'rb'), 'application/json'),
                #'openapi': ('simplecalculator_1.0.0.yaml', open('./temp-ws/BUILD-WS-3/simplecalculator_1.0.0.yaml', 'rb'), 'application/json')
            }
        )
        """
        """ for single product with multiple APIs"""
        #multiple_files = [('product',('mybank_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/mybank_1.0.0.yaml', 'rb'), 'application/json')),('openapi', ('accounts_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/accounts_1.0.0.yaml', 'rb'), 'application/json')),('openapi', ('payments_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/payments_1.0.0.yaml', 'rb'), 'application/json')),('openapi', ('secapp_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/secapp_1.0.0.yaml', 'rb'), 'application/json'))]
        #WORKING
        #multiple_files = [('product',(product_file_name + '.yaml', open(env_local_target_dir + product_file_name + '.yaml', 'rb'), 'application/json')),('openapi', ('accounts_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/accounts_1.0.0.yaml', 'rb'), 'application/json')),('openapi', ('payments_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/payments_1.0.0.yaml', 'rb'), 'application/json')),('openapi', ('secapp_1.0.0.yaml', open('./temp-ws/BUILD-WS-4/secapp_1.0.0.yaml', 'rb'), 'application/json'))]
        
        product_file_name = product_file_name + '.yaml'
        
        print("product_file_name:")
        print(product_file_name)
        multiple_files = [('product',(product_file_name, open(env_local_target_dir + "/" + product_file_name, 'rb'), 'application/json'))]
        print("multiple_files:")
        print(multiple_files)
        
        var_apilist = get_api_refs_from_product(env_local_target_dir, product_file_name)
        
        
        
        print("var_apilist:")
        print(var_apilist)
        
        if var_apilist:
            print(INFO + "Publish product:", product_file_name)
            print(INFO + "with APIs:", var_apilist)
            for apiname in var_apilist:
                multiple_files.append(('openapi', (apiname + '.yaml', open(env_local_target_dir+ "/" + apiname + '.yaml', 'rb'), 'application/json')))

            reqheaders = {
                "Accept" : "application/json",
                "Authorization" : "Bearer " + var_bearer_token
            }

            s = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
            s.mount(url, HTTPAdapter(max_retries=retries))
            #response = s.post(url, headers=reqheaders, data=multipart_data, verify=False, timeout=120)
            response = s.post(url, headers=reqheaders, files=multiple_files, verify=False, timeout=300)
            print(INFO + "Response:",response.status_code)
            resp_json = response.json()
        else:
            print(INFO + "Publish product:", product_file_name)
            print(INFO + "No APIs found for this product")
            resp_json = {
                "errorresponse" : "no APIs in product yaml - " + product_file_name
            }

    except Exception as e:
        resp_json = {
            "errorresponse" : e
        }
    
    return resp_json

def orchestrate():
    try:

        toolkit_credentials = utils.get_toolkit_credentials(os.environ["CONFIG_FILES_DIR"])
        environment_config = utils.get_env_config(os.environ["CONFIG_FILES_DIR"])

        var_product_tuple = raw_file_download_from_git.get_all_file_names_from_git_enterprise(os.environ["GIT_PRODUCTS_APIS_URL"],
                                                                                            os.environ["GIT_PRODUCTS_APIS_BRANCH"],
                                                                                            os.environ["GIT_PRIV_TOKEN"],
                                                                                            os.environ['GIT_PRODUCTS_PATH'])

        print("GET TOKEN:")
        print(environment_config["APIC_PLATFORM_API_URL"] + "/api",
                                                                os.environ["PROV_ORG_OWNER_USERNAME"],
                                                                os.environ["PROV_ORG_OWNER_PASSWORD"],
                                                                os.environ["PROV_ORG_REALM"],
                                                                toolkit_credentials["toolkit"]["client_id"],
                                                                toolkit_credentials["toolkit"]["client_secret"])
        
        
        gbt_resp = apic_platform_get_bearer_token.get_bearer_token(environment_config["APIC_PLATFORM_API_URL"] + "/api",
                                                                   os.environ["PROV_ORG_OWNER_USERNAME"],
                                                                   os.environ["PROV_ORG_OWNER_PASSWORD"],
                                                                   os.environ["PROV_ORG_REALM"],
                                                                   toolkit_credentials["toolkit"]["client_id"],
                                                                   toolkit_credentials["toolkit"]["client_secret"])


        print("TOKEN:")
        print(gbt_resp['access_token'])
        
        if "access_token" in gbt_resp:
            var_bearer_token = gbt_resp['access_token']
            """
            Ideally, you would query your catalog for existing products and APIs and compare these with the Products and APIs existing in your GitHub repo that will get published.
            Those existing Products and APIs in your catalog that are no longer in your Products and APIs GitHub repo should get deleted before.
            This way, your catalog Products and APIs will be in sync with your Products and APIs in your GitHub repository simulation some sort of GitOps approach for describing
            what is in your APIC instance through GitHub. See at the bottom of this script for more info
            """
            # Delete all the products first so that the bulk update approach works (this will delete all APIs too).
            
            # delete_all_products(environment_config["APIC_PLATFORM_API_URL"] + "/api",
            #                                 os.environ["PROV_ORG_TITLE"].strip().replace(" ","-").lower(),
            #                                 os.environ["PROV_ORG_CATALOG_NAME"], 
            #                                 var_bearer_token)
            
            
            
            apic_publish_audit = {}
            for product_file_name in var_product_tuple:
                publish_resp = publish_to_catalog_using_platform_api(environment_config["APIC_PLATFORM_API_URL"] + "/api",
                                                                    os.environ["PROV_ORG_TITLE"].strip().replace(" ","-").lower(),
                                                                    os.environ["PROV_ORG_CATALOG_NAME"], 
                                                                    WORKING_DIR_BASIC,
                                                                    product_file_name,
                                                                    var_bearer_token)
                
                print("publish_resp: ",publish_resp)
                if "errorresponse" in publish_resp:
                    apic_publish_audit[product_file_name] = "FAILED" + publish_resp['errorresponse']
                elif "state" in publish_resp:
                    apic_publish_audit[product_file_name] = "SUCCESS"
                else:
                    apic_publish_audit[product_file_name] = "FAILED" + publish_resp['errorresponse']
            
            print(INFO + "apic_publish_audit: ",apic_publish_audit)
            Audit_res.update_apic_publish_audit(WORKING_DIR_BASIC, apic_publish_audit)
            
            isSuccess = True
            for key,value in apic_publish_audit.items():
                if "FAILED" in value:
                    isSuccess = False

            if isSuccess == True:
                Audit_res.update_stage_res(WORKING_DIR_BASIC, "Products_API_publish", "SUCCESS")
                print(INFO + "Products_API_publish SUCCESS")
            else:
                raise Exception("An error occurred publishing a product or API")
        else:
            raise Exception("An error occurred getting the bearer token: " + json.dumps(gbt_resp))
    except Exception as e:
        Audit_res.update_stage_res(WORKING_DIR_BASIC, "Products_API_publish", "FAILED")
        raise Exception("[ERROR] - Exception in " + FILE_NAME + ": " + repr(e))



orchestrate()

"""
******************************
** Delete Products and APIs **
******************************

These are the following APIs needed to delete products and APIs on a fine-grained manner:

Get BEARER_TOKEN
----------------
BEARER_TOKEN = curl -k -X POST -d '{"username": "os.environ[PROV_ORG_OWNER_USERNAME]", "password": "os.environ[PROV_ORG_OWNER_PASSWORD]", "realm": "os.environ["PROV_ORG_REALM"]", "client_id": "toolkit_credentials["toolkit"]["client_id"]", "client_secret": "toolkit_credentials["toolkit"]["client_secret"]", "grant_type": "password"}' -H 'Content-Type: application/json' -H 'Accept: application/json' environment_config["APIC_PLATFORM_API_URL"] + "/api/token"


Get Catalogs
------------
curl environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs" -H 'Accept: application/json' -H 'Authorization: Bearer <BEARER_TOKEN>' --insecure


Get Orgs
--------
curl environment_config["APIC_PLATFORM_API_URL"] + "/api/orgs -H 'Accept: application/json' -H 'Authorization: Bearer <BEARER_TOKEN>' --insecure


Get Products
------------
curl environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs/<ORG_NAME_OR_ID>/<CATALOG_NAME_OR_ID>/products" -H 'accept: application/json' -H 'authorization: Bearer <BEARER_TOKEN>' --insecure


Get APIs
--------
curl environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs/<ORG_NAME_OR_ID>/<CATALOG_NAME_OR_ID>/apis" -H 'accept: application/json' -H 'authorization: Bearer <BEARER_TOKEN>' --insecure


Take an API offline
-------------------
curl -X 'PATCH' environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs/<ORG_NAME_OR_ID>/<CATALOG_NAME_OR_ID>/apis/<API_NAME_OR_ID>" -H 'Accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Bearer <BEARER_TOKEN>' --data-raw '{"state":"offline"}' --insecure


Delete a product
----------------
curl -X DELETE environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs/<ORG_NAME_OR_ID>/<CATALOG_NAME_OR_ID>/products/<PRODUCT_NAME>?confirm=<CATALOG_NAME>" -H 'Accept: application/json' -H 'Authorization: Bearer <BEARER_TOKEN>' --insecure


Delete ALL Products
-------------------
curl -X DELETE environment_config["APIC_PLATFORM_API_URL"] + "/api/catalogs/<ORG_NAME_OR_ID>/<CATALOG_NAME_OR_ID>/products?confirm=<CATALOG_NAME>" -H 'Accept: application/json' -H 'Authorization: Bearer <BEARER_TOKEN>' --insecure


More info on APIC management REST endpoints:
https://apic-api.apiconnect.ibmcloud.com/v10/?_ga=2.233587928.752341463.1623867527-1939642083.1623276281
"""
