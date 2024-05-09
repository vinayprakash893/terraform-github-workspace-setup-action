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
        ws_api.list(page=None, page_size=None, include=None, search=None, filters=None)
        print(ws_api.list)
        print("---vny---")
        ws_api.create(ws_payload)
        logging.info(f"Workspace {WORKSPACE_NAME} has been created.")
        print(f"Workspace {WORKSPACE_NAME} has been created.")
