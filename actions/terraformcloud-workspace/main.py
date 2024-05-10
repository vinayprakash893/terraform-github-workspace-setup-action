import os
from terrasnek.api import TFC
import logging

class Context:
    def __init__(self, environ):
        self._variables = {}
        self._environ = environ

    def load_from_env(self):
        self._variables.update({'env': self._environ})

    def workspace_create(self):
        API_TOKEN = self._environ.get('INPUT_API_TOKEN')
        ORG_NAME = self._environ.get('INPUT_ORG_NAME')
        WORKSPACE_NAME = self._environ.get('INPUT_WORKSPACE_NAME')
        PROJECT_NAME = self._environ.get('INPUT_PROJECT_NAME')
        VARIABLESET_NAME = self._environ.get('INPUT_VARIABLESET_NAME')
        tfc = TFC(API_TOKEN)
        tfc.set_org(ORG_NAME)
        ws_api = tfc.workspaces
        # List existing Projects
        prj_api = tfc.projects
        project_filters = [
        {
                        "keys": ["name"], # ends up as ["workspace"]["name"]
                        "value": PROJECT_NAME
        }
        ]
        existing_projects = prj_api.list_all(filters=None, query=None)
        project_id = None
        for prj in existing_projects["data"]:
            if prj["attributes"]["name"] == PROJECT_NAME:
                project_id = prj["id"]
                break
        project_exists = any(prj["attributes"]["name"] == PROJECT_NAME for prj in existing_projects["data"])
        if project_exists:
            print(f"Project '{PROJECT_NAME}' exists.")
        else:
            logging.info(f"Project '{PROJECT_NAME}' does not exist.")
            print(f"Project '{PROJECT_NAME}' does not exist.")
        # List existing workspaces
        existing_workspaces = ws_api.list(page=None, page_size=None, include=None, search=None, filters=None)
        workspace_exists = any(ws["attributes"]["name"] == WORKSPACE_NAME for ws in existing_workspaces["data"])
        if workspace_exists:
            logging.error(f"Workspace '{WORKSPACE_NAME}' already exists.")
            print(f"Workspace '{WORKSPACE_NAME}' already exists.")
            
        else:
            # Create Workspace
            ws_payload = {
                "data": {
                    "type": "workspaces",
                    "attributes": {
                        "name": WORKSPACE_NAME,
                        "auto-apply":"false",
                        "description":"Created by Github Actions for Terraform project"
                    },
                    "relationships": {
                        "project": {
                            "data": {
                                "type": "projects",
                                "id": project_id
                            }
                        }
                    }
                }
            }
            new_workspace = ws_api.create(ws_payload)
            workspace_id = new_workspace["data"]["id"]
            logging.info(f"Workspace {WORKSPACE_NAME} has been created.")
            print(f"Workspace {WORKSPACE_NAME} has been created.")
            print(f"WorkspaceID is {workspace_id} .")

            # Map Variable Set to Workspace
            vs_api = tfc.var_sets
            print( "mapping Variable set")
            ws_payload_id = {
                "data": [
                    {
                    "type": "workspaces",
                    "id": workspace_id
                    }
                ]
            }
            list_varsets = vs_api.list_for_org()
            variableset_id = None
            for varset in list_varsets["data"]:
                if varset["attributes"]["name"] == VARIABLESET_NAME:
                    variableset_id = varset["id"]
                    break
            if variableset_id:
                vs_api.apply_varset_to_workspace(variableset_id, ws_payload_id)
                print(f"Variable Set mapping completed {VARIABLESET_NAME} for workspace {WORKSPACE_NAME}.")
            else:
                logging.error(f"Variable Set '{VARIABLESET_NAME}' not found.")
                print(f"Variable Set '{VARIABLESET_NAME}' not found.")

