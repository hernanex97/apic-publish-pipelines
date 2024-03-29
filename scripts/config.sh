#!/bin/bash

#######################################
# Configuration Initialization Script #
#######################################

if [[ -z "$1" ]]
then
  echo "[ERROR][config.sh] - An IBM API Connect installation OpenShift poject was not provided"
  exit 1
else
  APIC_NAMESPACE=$1
  echo "IBM API Connect has been installed in the ${APIC_NAMESPACE} OpenShift project"
fi

# Make a configuration files directory
cd ..
rm -rf config
mkdir config
cd config

# Get the needed URLs for the automation
APIC_ADMIN_URL=`oc get routes -n ${APIC_NAMESPACE} | grep mgmt-admin |  awk '{print $2}'`
if [[ -z "${APIC_ADMIN_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Admin url"; exit 1; fi
APIC_API_MANAGER_URL=`oc get routes -n ${APIC_NAMESPACE} | grep api-manager |  awk '{print $2}'`
if [[ -z "${APIC_API_MANAGER_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Management url"; exit 1; fi
APIC_GATEWAY_URL=`oc get routes -n ${APIC_NAMESPACE} | grep gateway | grep -v manager | awk '{print $2}'`
if [[ -z "${APIC_GATEWAY_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Gateway url"; exit 1; fi
APIC_GATEWAY_MANAGER_URL=`oc get routes -n ${APIC_NAMESPACE} | grep gateway-manager | awk '{print $2}'`
if [[ -z "${APIC_GATEWAY_MANAGER_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Gateway Manager url"; exit 1; fi
# APIC_ANALYTICS_CONSOLE_URL=`oc get routes -n ${APIC_NAMESPACE} | grep ac-endpoint | awk '{print $2}'`
# if [[ -z "${APIC_ANALYTICS_CONSOLE_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Analytics Console url"; exit 1; fi
# APIC_PORTAL_DIRECTOR_URL=`oc get routes -n ${APIC_NAMESPACE} | grep portal-director | awk '{print $2}'`
# if [[ -z "${APIC_PORTAL_DIRECTOR_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Portal Director url"; exit 1; fi
# APIC_PORTAL_WEB_URL=`oc get routes -n ${APIC_NAMESPACE} | grep portal-web | awk '{print $2}'`
# if [[ -z "${APIC_PORTAL_WEB_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Portal Web url"; exit 1; fi
APIC_PLATFORM_API_URL=`oc get routes -n ${APIC_NAMESPACE} | grep platform-api | awk '{print $2}'`
if [[ -z "${APIC_PLATFORM_API_URL}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Platform API url"; exit 1; fi

# Storing the urls in the JSON config file
echo "{" >> config.json
echo "\"APIC_ADMIN_URL\":\"${APIC_ADMIN_URL}\"," >> config.json
echo "\"APIC_API_MANAGER_URL\":\"${APIC_API_MANAGER_URL}\"," >> config.json
echo "\"APIC_GATEWAY_URL\":\"${APIC_GATEWAY_URL}\"," >> config.json
echo "\"APIC_GATEWAY_MANAGER_URL\":\"${APIC_GATEWAY_MANAGER_URL}\"," >> config.json
# echo "\"APIC_ANALYTICS_CONSOLE_URL\":\"${APIC_ANALYTICS_CONSOLE_URL}\"," >> config.json
# echo "\"APIC_PORTAL_DIRECTOR_URL\":\"${APIC_PORTAL_DIRECTOR_URL}\"," >> config.json
# echo "\"APIC_PORTAL_WEB_URL\":\"${APIC_PORTAL_WEB_URL}\"," >> config.json
echo "\"APIC_PLATFORM_API_URL\":\"${APIC_PLATFORM_API_URL}\"," >> config.json


# Get the IBM APIC Connect Cloud Manager Admin password
# APIC_ADMIN_PASSWORD=$(oc get secret $(oc get secrets -n ${APIC_NAMESPACE} | grep mgmt-admin-pass | awk '{print $1}') -n ${APIC_NAMESPACE} -o jsonpath='{.data.password}' | base64 -d)
MGMT_PASSWORD=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_OWNER_PASSWORD}' | base64 --decode)
if [[ -z "${MGMT_PASSWORD}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG password"; exit 1; fi

MGMT_USER=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_OWNER_USERNAME}' | base64 --decode)
if [[ -z "${MGMT_USER}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG Username"; exit 1; fi

PROV_REALM=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_REALM}' | base64 --decode)
if [[ -z "${PROV_REALM}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG Realm"; exit 1; fi


# Get the APIC CLI
echo "curl -s --write-out '%{http_code}' https://${APIC_API_MANAGER_URL}/client-downloads/toolkit-linux.tgz --insecure --output toolkit-linux.tgz"
HTTP_CODE=`curl -s --write-out '%{http_code}' https://${APIC_API_MANAGER_URL}/client-downloads/toolkit-linux.tgz --insecure --output toolkit-linux.tgz`
if [[ "${HTTP_CODE}" != "200" ]]
then 
  echo "[ERROR][config.sh] - An error ocurred downloading the APIC toolkit to get the APIC CLI"
  exit 1
fi
tar -xvf toolkit-linux.tgz
# chmod +x apic-slim
chmod 777 apic-slim

echo "APIC accept licenses"
echo "y" | ./apic-slim
echo "y" | ./apic-slim

echo "apic-slim directory"
pwd
ll

# Get the IBM APIC Connect Cloud Manager Admin password
# APIC_ADMIN_PASSWORD=$(oc get secret $(oc get secrets -n ${APIC_NAMESPACE} | grep mgmt-admin-pass | awk '{print $1}') -n ${APIC_NAMESPACE} -o jsonpath='{.data.password}' | base64 -d)
MGMT_PASSWORD=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_OWNER_PASSWORD}' | base64 --decode)
if [[ -z "${MGMT_PASSWORD}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG password"; exit 1; fi

MGMT_USER=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_OWNER_USERNAME}' | base64 --decode)
if [[ -z "${MGMT_USER}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG Username"; exit 1; fi

PROV_REALM=$(oc get secret apic-pipeline-provider-org -n ${APIC_NAMESPACE} -o jsonpath='{.data.PROV_ORG_REALM}' | base64 --decode)
if [[ -z "${PROV_REALM}" ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect ORG Realm"; exit 1; fi

# Store the IBM APIC Connect Cloud Manager Admin password in the JSON config file
echo "\"APIC_ADMIN_PASSWORD\":\"${MGMT_PASSWORD}\"" >> config.json
echo "}" >> config.json

# Login to IBM API Connect Cloud Manager through the APIC CLI
./apic-slim login --server ${APIC_API_MANAGER_URL} --username ${MGMT_USER} --password ''"${MGMT_PASSWORD}"'' --realm ${PROV_REALM} --accept-license > /dev/null
if [[ $? -ne 0 ]]; then echo "[ERROR][config.sh] - An error ocurred login into IBM API Connect using the APIC CLI"; exit 1; fi

# Get the toolkit credentials
./apic-slim cloud-settings:toolkit-credentials-list --server ${APIC_API_MANAGER_URL} --format json > toolkit-creds.json
if [[ $? -ne 0 ]]; then echo "[ERROR][config.sh] - An error ocurred getting the IBM API Connect Toolkit Credentials using the APIC CLI"; exit 1; fi

# DEBUG information
if [[ ! -z "${DEBUG}" ]]
then
  echo "This is the environment configuration"
  echo "-------------------------------------"
  cat config.json
  echo "These are the IBM API Connect ToolKit Credentials"
  echo "-------------------------------------------------"
  cat toolkit-creds.json
fi
