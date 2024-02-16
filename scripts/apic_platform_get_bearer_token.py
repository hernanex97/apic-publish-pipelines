import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

FILE_NAME = "apic_platform_get_bearer_token.py"
INFO = "[INFO]["+ FILE_NAME +"] - " 

def get_bearer_token(apic_platform_base_url, apic_mgmt_username, apic_mgmt_password, apic_mgmt_realm, apic_rest_clientid, apic_rest_clientsecret): 
    try:
        url = "https://" + apic_platform_base_url + "/token"
        reqheaders = {
            "Content-Type" : "application/json",
            "Accept" : "application/json"
        }

        reqJson = {
            "username": apic_mgmt_username,
            "password": apic_mgmt_password,
            "realm": apic_mgmt_realm,
            "client_id": apic_rest_clientid,
            "client_secret": apic_rest_clientsecret,
            "grant_type": "password"
        }
        print(INFO + "Get Bearer Token")
        print(INFO + "----------------")
        print(INFO + "Url:", url)
        print(INFO + "Username:", apic_mgmt_username)
        print(INFO + "Client ID:", apic_rest_clientid)
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
        s.mount(apic_platform_base_url, HTTPAdapter(max_retries=retries))

        response = s.post(url, headers=reqheaders, json=reqJson, verify=False, timeout=20)
        resp_json = response.json()
        return resp_json
    except Exception as e:
        err_resp = {
            "errorresponse" : e
        }
        print(type(e))
        return err_resp
