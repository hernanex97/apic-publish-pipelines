pipeline {
    agent any
    parameters {
        text(name: 'json_req', description: 'json input with apic platform, productname details', defaultValue: '{"appModule": "all", "appname": "all", "productnames": ["retail-single-payment-open-banking-standard_1.0.0", "corp-multi-payment-online-open-banking-standard_1.0.0", "accounts-open-banking-standard_1.0.0"], "deploytype": "new", "env": "sandbox", "deploymentPlatform": {"domain": ".dteroks0914xaqz6-4b4a324f027aea19c5cbc0c3275c4656-0000.hkg02.containers.appdomain.cloud", "acenamespace": "idbp", "appnamespace": "idbp-sandbox", "apic": {"mgmt": {"platformBaseURL": "https://ademo-mgmt-platform-api-idbp.dteroks0914xaqz6-4b4a324f027aea19c5cbc0c3275c4656-0000.hkg02.containers.appdomain.cloud/api", "realm": "provider/default-idp-2", "username": "ananth.mkh", "pswd": "zaq1!QAZ", "provOrg": "idbp-test", "catalogName": "dev"}, "gwyBaseURL": "https://ademo-gw-gateway-idbp.dteroks0914xaqz6-4b4a324f027aea19c5cbc0c3275c4656-0000.hkg02.containers.appdomain.cloud/idbp-test/dev"} }, "auditTarget": {"type": "db", "ELK": {"address": "ELK_address", "port": "ELK_port", "authentication": {"type": "creds", "creds": {"username": "ELK_username", "pswd": "ELK_pswd"} } }, "db": {"address": "sandbox-auditdb-v1", "port": "3306", "authentication": {"type": "creds", "creds": {"username": "db username here", "pswd": "db pswd here"} } } } }')
    }
    stages {
        stage('Initialize Build') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                        python3 initialize_apic_deploy.py
                    '''
                }
                
            }
        }
        stage('Download Products Yamls from Git') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                        python3 download_product_files_from_git.py
                    '''
                }
                
            }
        }
        stage('Download APIs Yaml from Git') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                        python3 download_api_files_from_git.py
                    '''
                }
                
            }
        }
        stage('Apply ENV Values to API YAML') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                        python3 replace_api_yaml_env_param.py
                    '''
                }
                
            }
        }
        stage('Publish Products to Target APIC Enviornment') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                        python3 apic_platform_publish_to_catalog.py
                    '''
                }
                
            }
        }
        stage('Test Published APIs') {
            steps {
                dir("${WORKSPACE}/scripts"){
                    sh '''
                    echo "    python3 test_apic_apis.py"
                    '''
                }
                
            }
        }
    }
}
