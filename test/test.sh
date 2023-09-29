#!/bin/sh -l
clear
key=""access_key_id""
printf "\nDelete variable %s" "$key"
id=$(cat vars.json | jq -r --arg key "$key" '.data[] | select(.attributes.key == $key) | .id')
printf "\nDelete variable %s" "$id"



json_data=$(cat vars.json)

data_array=($(jq -c '.data[]' <<< "$json_data"))

# Initialize the ID variable
id=""

# Iterate through the array and find the matching key
for data in "${data_array[@]}"; do
    data_key=$(jq -r '.attributes.key' <<< "$data")
    if [[ "$data_key" == "$key" ]]; then
        id=$(jq -r '.id' <<< "$data")
        break  # Exit the loop when a match is found
    fi
done

printf "\nNewID variable %s" "$id"