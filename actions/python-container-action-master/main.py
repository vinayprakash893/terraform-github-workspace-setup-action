import os
import json
import requests

# TF_ORGA = os.getenv("TF_ORGA")
# TF_WS = os.getenv("TF_WS")
# TF_TOKEN = os.getenv("TF_TOKEN")
# TF_HOST = os.getenv("TF_HOST")
# TF_PRJ = os.getenv("TF_PRJ")
# TF_VARSET = os.getenv("TF_VARSET")

TF_ORGA = 'Cloudtech'
TF_WS = 'vnytest4'
TF_TOKEN = os.environ["INPUT_MYINPUT"]
TF_HOST = "app.terraform.io"
TF_PRJ = 'prj-e9V6rDjNezrrq1Em'
TF_VARSET = 'varset-CfEeJ5NPqiebXaCg'

# # Write variables to a JSON file
# with open('variables.json', 'w') as f:
#     json.dump({"vars": json.loads(os.getenv("VAR_JSON"))}, f)

# Create workspace
print("\nCreate or get workspace:", TF_WS)
with open('/tmp/workspace.payload') as f:
    workspace_payload = f.read().replace('T_WS', TF_WS).replace('T_PRJ', TF_PRJ)
with open('workspace.json', 'w') as f:
    f.write(workspace_payload)

workspace_response = requests.post(f"https://{TF_HOST}/api/v2/organizations/{TF_ORGA}/workspaces",
                                   headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"},
                                   data=workspace_payload)
with open('logs.txt', 'wb') as f:
    f.write(workspace_response.content)

# Retrieve Workspace ID
workspace_id_response = requests.get(f"https://{TF_HOST}/api/v2/organizations/{TF_ORGA}/workspaces/{TF_WS}",
                                      headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"})
wid = workspace_id_response.json()['data']['id']

# Map Variable Set to workspace
with open('/tmp/workspaceid.payload') as f:
    workspaceid_payload = f.read().replace('T_WS_ID', wid)
workspaceid_response = requests.post(f"https://{TF_HOST}/api/v2/varsets/{TF_VARSET}/relationships/workspaces",
                                     headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"},
                                     data=workspaceid_payload)
with open('logs.txt', 'ab') as f:
    f.write(workspaceid_response.content)

# Clean only replacing variables
fullvars_response = requests.get(f"https://{TF_HOST}/api/v2/workspaces/{wid}/vars",
                                 headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"})
fullvars_json = fullvars_response.json()
# variables_json = json.loads(os.getenv("VAR_JSON"))
for var in variables_json["vars"]:
    key = var["key"]
    id = next((item['id'] for item in fullvars_json['data'] if item['attributes']['key'] == key), None)
    if id:
        print(f"\nDeleting variable {key}")
        delete_response = requests.delete(f"https://{TF_HOST}/api/v2/workspaces/{wid}/vars/{id}",
                                          headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"})
        print(f"\nVariable ID {id}")

# Create variables
for var in variables_json["vars"]:
    key = var["key"]
    value = var["value"]
    sensitive = var.get("sensitive", False)
    print(f"\nCreate variable {key}")
    payload = {
        "data": {
            "type": "vars",
            "attributes": {
                "key": key,
                "value": value,
                "sensitive": sensitive,
                "hcl": False
            },
            "relationships": {
                "workspace": {
                    "data": {
                        "id": wid,
                        "type": "workspaces"
                    }
                }
            }
        }
    }
    create_response = requests.post(f"https://{TF_HOST}/api/v2/workspaces/{wid}/vars",
                                    headers={"Authorization": f"Bearer {TF_TOKEN}", "Content-Type": "application/vnd.api+json"},
                                    json=payload)
    with open('log.txt', 'ab') as f:
        f.write(create_response.content)

print("\n\n")
print("::set-output name=workspace_id::", wid)
