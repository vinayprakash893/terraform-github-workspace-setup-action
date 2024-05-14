import os
from terrasnek.api import TFC
import logging
import json

logging.basicConfig(level=logging.INFO)

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

        # Get the TFC project_id
        project_id = self._get_tfc_project_id(tfc, PROJECT_NAME)

        #find or create the TFC workspace
        workspace = self._find_tfc_workspace(tfc, project_id, WORKSPACE_NAME)

        #check variable set is null or not
        if VARIABLESET_NAME:
            # Get the terraform cloud variable set
            var_set_id = self._get_tfc_var_set_id(tfc, VARIABLESET_NAME)

            # Apply the Terraform Cloud variable set to the workspace
            self._apply_var_set_to_tfc_workspace(tfc, var_set_id, workspace['id'])      

    def _get_tfc_project_id(self, TFC, project_name):
        try:
            logging.info(f"Fetching TFC project: {project_name}")

            project = TFC.projects.list_all(
                filters=[{
                    'keys': ['names'],
                    'value': project_name
                }]
            ).get('data', None)

            if not project:
                logging.error(f"TFC project not found: {project_name}")

            logging.info(f"project: {json.dumps(project)}")

            project_id = None
            for prj in project:
                if prj["attributes"]["name"] == project_name:
                    project_id = prj["id"]
                    break

            return project_id

        except Exception as e:
            logging.error(f"Failed to fetch TFC project: {str(e)}")
            raise


    def _get_tfc_workspace(self, TFC, workspace_name):
        try:
            logging.info(f"Getting TFC workspace: {workspace_name}")

            workspace = TFC.workspaces.list_all(
                filters=[{
                'keys': ['workspace', 'name'],
                'value': workspace_name
                }]
            ).get('data', None)

            if not workspace:
                logging.error(f"TFC workspace not found: {workspace_name}")

            logging.info(f"workspace: {json.dumps(workspace)}")
            for ws in workspace:
                if ws["attributes"]["name"] == workspace_name:
                    workspace = ws
                    break

            return workspace

        except Exception as e:
            logging.error(f"Failed to get TFC workspace: {str(e)}")
            raise

    def _create_TFC_workspace(self, TFC, project_id, workspace_name):
        logging.info(f"Creating TFC workspace: {workspace_name}")

        try:
            workspace = TFC.workspaces.create({
                'data': {
                'type': 'workspaces',
                'attributes': {
                    'auto-apply': 'false',
                    'name': workspace_name
                },
                'relationships': {
                    'project': {
                    'data': {
                        'id': project_id,
                        'type': 'projects'
                    }
                    }
                }
                }
            })['data']
            logging.info(f"workspace: {json.dumps(workspace)}")
            
            return workspace

        except Exception as e:
            logging.error(f"Failed to create TFC workspace: {workspace_name}")
            logging.error(str(e))
            raise


    def _find_tfc_workspace(self, TFC, project_id, workspace_name):
        logging.info('Checking if tfc workspace already exists')

        workspace = None

        workspace = self._get_tfc_workspace(TFC, workspace_name)
        # If workspace not found, create a new workspace
        if not workspace: 
            workspace = self._create_TFC_workspace(TFC, project_id, workspace_name)

        return workspace


    def _get_tfc_var_set_id(self, TFC, var_set_name):
        try:
            logging.info(f"Getting TFC variable set: {var_set_name}")

            var_set_id = None
            var_sets = TFC.var_sets.list_all_for_org().get('data', [])

            for vs in var_sets:
                if vs['attributes']['name'] == var_set_name:
                    var_set_id = vs['id']
                    break

            if not var_set_id:
                logging.error(f"TFC variable set not found: {var_set_name}")

            logging.info(f"var_sets: {json.dumps(var_sets)}")

            return var_set_id

        except Exception as e:
            logging.error(f"Failed to get TFC variable set: {str(e)}")
            raise


    def _apply_var_set_to_tfc_workspace(self, TFC, var_set_id, workspace_id):
        try:
            logging.info(f"Applying the variable set to the workspace")

            response = TFC.var_sets.apply_varset_to_workspace(
                varset_id=var_set_id,
                payload={
                    'data': [{
                        'id': workspace_id,
                        'type': 'workspaces'
                    }]
                }
            )
            logging.info(f"response: {response}")

        except Exception as e:
            logging.error(f"Failed to apply variable set to workspace: {str(e)}")
            raise



# import os
# from terrasnek.api import TFC
# import logging

# class Context:
#     def __init__(self, environ):
#         self._variables = {}
#         self._environ = environ

#     def load_from_env(self):
#         self._variables.update({'env': self._environ})

#     def workspace_create(self):
#         API_TOKEN = self._environ.get('INPUT_API_TOKEN')
#         ORG_NAME = self._environ.get('INPUT_ORG_NAME')
#         WORKSPACE_NAME = self._environ.get('INPUT_WORKSPACE_NAME')
#         PROJECT_NAME = self._environ.get('INPUT_PROJECT_NAME')
#         VARIABLESET_NAME = self._environ.get('INPUT_VARIABLESET_NAME')
#         tfc = TFC(API_TOKEN)
#         tfc.set_org(ORG_NAME)
#         ws_api = tfc.workspaces
#         # List existing Projects
#         prj_api = tfc.projects
#         project_filters = [
#         {
#                         "keys": ["name"], # ends up as ["workspace"]["name"]
#                         "value": PROJECT_NAME
#         }
#         ]
#         existing_projects = prj_api.list_all(filters=project_filters, query=None)
#         project_id = None
#         for prj in existing_projects["data"]:
#             if prj["attributes"]["name"] == PROJECT_NAME:
#                 project_id = prj["id"]
#                 break
#         project_exists = any(prj["attributes"]["name"] == PROJECT_NAME for prj in existing_projects["data"])
#         if project_exists:
#             print(f"Project '{PROJECT_NAME}' exists.")
#         else:
#             logging.info(f"Project '{PROJECT_NAME}' does not exist.")
#             print(f"Project '{PROJECT_NAME}' does not exist.")
#         # List existing workspaces
#         workspace_filters = [
#         {
#                         "keys": ["Project", "id"], # ends up as ["workspace"]["name"]
#                         "value": project_id
#         }
#         ]
#         existing_workspaces = ws_api.list_all(search=None, include=None, filters=workspace_filters)
#         workspace_exists = any(ws["attributes"]["name"] == WORKSPACE_NAME for ws in existing_workspaces["data"])
#         if workspace_exists:
#             logging.error(f"Workspace '{WORKSPACE_NAME}' already exists.")
#             print(f"Workspace '{WORKSPACE_NAME}' already exists.")
            
#         else:
#             # Create Workspace
#             ws_payload = {
#                 "data": {
#                     "type": "workspaces",
#                     "attributes": {
#                         "name": WORKSPACE_NAME,
#                         "auto-apply":"false",
#                         "description":"Created by Github Actions for Terraform project"
#                     },
#                     "relationships": {
#                         "project": {
#                             "data": {
#                                 "type": "projects",
#                                 "id": project_id
#                             }
#                         }
#                     }
#                 }
#             }
#             new_workspace = ws_api.create(ws_payload)
#             workspace_id = new_workspace["data"]["id"]
#             logging.info(f"Workspace {WORKSPACE_NAME} has been created.")
#             print(f"Workspace {WORKSPACE_NAME} has been created.")
#             print(f"WorkspaceID is {workspace_id} .")

#             # Map Variable Set to Workspace
#             vs_api = tfc.var_sets
#             print( "mapping Variable set")
#             ws_payload_id = {
#                 "data": [
#                     {
#                     "type": "workspaces",
#                     "id": workspace_id
#                     }
#                 ]
#             }
#             list_varsets = vs_api.list_for_org()
#             variableset_id = None
#             for varset in list_varsets["data"]:
#                 if varset["attributes"]["name"] == VARIABLESET_NAME:
#                     variableset_id = varset["id"]
#                     break
#             if variableset_id:
#                 vs_api.apply_varset_to_workspace(variableset_id, ws_payload_id)
#                 print(f"Variable Set mapping completed {VARIABLESET_NAME} for workspace {WORKSPACE_NAME}.")
#             else:
#                 logging.error(f"Variable Set '{VARIABLESET_NAME}' not found.")
#                 print(f"Variable Set '{VARIABLESET_NAME}' not found.")

