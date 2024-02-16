import yaml
import glob
import os

def get_basepath_from_api(target_dir):
    yamlFiles=glob.glob(target_dir + "/*.yaml")

    var_api_basepath_list = {}
    for ymlFile in yamlFiles:
        with open(ymlFile) as f:
            # use safe_load instead load
            dataMap = yaml.safe_load(f)
            if "basePath" in dataMap:
                var_api_name = os.path.basename(ymlFile).replace(".yaml","")
                var_api_basepath_list[var_api_name] = dataMap['basePath']
    return var_api_basepath_list
