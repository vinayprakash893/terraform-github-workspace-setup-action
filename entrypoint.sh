#!/bin/sh -l

TF_ORGA=$(echo $1)
TF_WS=$(echo $2)
TF_TOKEN=$(echo $3)
echo "{ \"vars\":[ $4 ]}" > variables.json
TF_HOST=$(echo $5)

#Create workspace
printf "\nCreate or get workspace:%s" "$TF_WS"
sed "s/T_WS/$TF_WS/" < /tmp/workspace.payload > workspace.json
curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" --request POST --data @workspace.json "https://$TF_HOST/api/v2/organizations/$TF_ORGA/workspaces" > logs.txt

#Retreive Workspace ID
wid=$(curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" "https://$TF_HOST/api/v2/organizations/$TF_ORGA/workspaces/$TF_WS" | jq -r .data.id)

# #Clean existing all variables
# printf "\nClear existing variables"
# curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" "https://$TF_HOST/api/v2/workspaces/$wid/vars" > vars.json
# x=$(cat vars.json | jq -r ".data[].id" | wc -l | awk '{print $1}')
# i=0
# while [ $i -lt $x ]
# do
#   curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" --request DELETE "https://$TF_HOST/api/v2/workspaces/$wid/vars/$(cat vars.json | jq -r ".data[$i].id")" > logs.txt
#   i=`expr $i + 1`  
# done

#Clean only replacing variables
curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" "https://$TF_HOST/api/v2/workspaces/$wid/vars" > fullvars.json
for k in $(jq '.vars | keys | .[]' variables.json); do
    value=$(jq -r ".vars[$k]" variables.json);

    key=$(echo $value | jq '.key')
    raw_value=$(echo $value | jq '.value')
    escaped_value=$(echo $raw_value | sed -e 's/[]\/$*.^[]/\\&/g');
    sensitive=$(echo $value | jq '.sensitive')

    printf "\nDelete variable %s" "$key"
    # id=$(cat vars.json | jq -r --arg key "$key" '.data[] | select(.attributes.key == $key) | .id')
    id=$(cat vars.json | jq -r --arg key "$key" '.data[]' )
    printf "\nNewID variable %s" "$id"
    printf "\n"
    #curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" --request DELETE "https://$TF_HOST/api/v2/workspaces/$wid/vars/$id"
    printf "\nDeleted variable %s" "$key"
done

#Create variables

for k in $(jq '.vars | keys | .[]' variables.json); do
    value=$(jq -r ".vars[$k]" variables.json);

    key=$(echo $value | jq '.key')
    raw_value=$(echo $value | jq '.value')
    escaped_value=$(echo $raw_value | sed -e 's/[]\/$*.^[]/\\&/g');
    sensitive=$(echo $value | jq '.sensitive')

    printf "\nCreate variable %s" "$key"
    
    sed -e "s/T_KEY/$key/" -e "s/my-hcl/false/" -e "s/T_VALUE/$escaped_value/" -e "s/T_SECURED/$sensitive/" -e "s/T_WSID/$wid/" < /tmp/variable.payload  > paylaod.json
    curl -s --header "Authorization: Bearer $TF_TOKEN" --header "Content-Type: application/vnd.api+json" --request POST --data @paylaod.json "https://$TF_HOST/api/v2/workspaces/$wid/vars" > log.txt
done

printf "\n\n"
echo "::set-output name=workspace_id::$wid"
