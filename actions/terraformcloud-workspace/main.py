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
                    "id": PROJECT_NAME
                    }
                }
                }
            }
        }
        
        # List existing workspaces
        existing_workspaces = ws_api.list(page=None, page_size=None, include=None, search=None, filters=None)
        workspace_exists = any(ws["attributes"]["name"] == WORKSPACE_NAME for ws in existing_workspaces["data"])
        if workspace_exists:
            logging.error(f"Workspace '{WORKSPACE_NAME}' already exists.")
            print(f"Workspace '{WORKSPACE_NAME}' already exists.")
            return
        # Create Workspace
        new_workspace = ws_api.create(ws_payload)
        workspace_id = new_workspace["data"]["id"]
        logging.info(f"Workspace {WORKSPACE_NAME} has been created.")
        print(f"Workspace {WORKSPACE_NAME} has been created.")

        # Map Variable Set to Workspace
        print( "mapping Variable set")
        ws_payload_id = {
            "data": [
                {
                "type": "workspaces",
                "id": workspace_id
                }
            ]
        }
        ws_api.apply_varset_to_workspace(VARIABLESET_NAME, ws_payload_id)
