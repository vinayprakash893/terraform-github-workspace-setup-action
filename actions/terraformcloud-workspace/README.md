<!-- [![release](https://img.shields.io/github/v/release/cuchi/jinja2-action?style=flat-square)](vvvv)
[![marketplace](https://img.shields.io/badge/marketplace-jinja2--action-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/jinja2-action) -->

# Terraform Cloud Workspace Creation GitHub Action

This GitHub Action automates the creation of a Terraform Cloud workspace and maps a specified variable set to the workspace. It utilizes a Python Docker image to execute the necessary tasks.

## Features:
* Can Create new workspace with `workspace_name`.
* Map Variable Set with Workspace created

## Inputs

- `api_token`
- `org_name`
- `workspace_name`
- `project_name`
- `variableset_name`

## Usage

1. Ensure you have the necessary API token from Terraform Cloud and the required permissions within your organization.
2. Store your sensitive data (API token) securely as GitHub secrets.
3. Configure the GitHub Action workflow file in your repository to utilize this action. See the example workflow file below.


```yaml
jobs:
  terraform_cloud_workspace:
    name: Create Terraform Cloud Workspace
    steps:
    - name: Create Terraform Cloud Workspace
      uses: location/actions/terraformcloud-workspace@main
      with:
        org_name: 'ORG_name'
        workspace_name: 'Workspace_Name'
        project_name: 'Project_name'
        variableset_name: 'Variable_set_name'
        api_token: ${{ secrets.TF_API_TOKEN }}
```

| Input Variable | Required | Default                       | Description                                                                                                              |
| -------------- | -------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
|api_token    | Yes       | `""`                      | API Token for Terraform Cloud authentication.
|org_name     | Yes       | `""`                      |   Name of the organization in Terraform Cloud.|
|workspace_name     | Yes       | `""`                 |  Name of the workspace to be created.|
|project_name     | Yes       | `""`                      |   Name of the project associated with the workspace.|
|variableset_name     | Optional       | `""`                      |  Name of the variable set to be mapped in the workspace.|


# See also
- [Terrasnek docs](https://terrasnek.readthedocs.io/en/latest/index.html)
- [Syntax](https://terrasnek.readthedocs.io/en/latest/common_patterns.html)
- [Examples](https://terrasnek.readthedocs.io/en/latest/examples.html)