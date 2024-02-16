import yaml
import glob
import os

def get_api_list_from_product(target_dir,var_product_tuple):
    try:
        yamlFiles=glob.glob(target_dir + "/*.yaml")

        var_apilist = []
        for ymlFile in yamlFiles:
            fileName = os.path.splitext(os.path.basename(ymlFile))
            if(fileName[0] in var_product_tuple):
                with open(ymlFile) as f:
                    # use safe_load instead load
                    dataMap = yaml.safe_load(f)
                    if "product" in dataMap and "apis" in dataMap:
                        for api_id, api_info in dataMap["apis"].items():
                            """
                            print("$ref value is : ", api_info["$ref"])
                            if not api_info["$ref"] in var_apilist:
                                var_apilist.append(api_info["$ref"])  
                            """
                            if "name" in api_info:
                                var_api_name = api_info["name"].replace(":","_")
                                var_api_name = var_api_name + ".yaml"
                                if not var_api_name in var_apilist:
                                    var_apilist.append(var_api_name)  
                            elif "$ref" in api_info:
                                if not api_info["$ref"] in var_apilist:
                                    var_apilist.append(api_info["$ref"])
        return var_apilist   
    except Exception as e:
        raise("[ERROR] - Error in parse_apic_product_yaml_get_api_names.py : " + repr(e))