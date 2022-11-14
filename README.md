# spec.opencdms.org

This repository contains the contents of the `spec.opencdms.org` GitHub pages site. Along with files and scripts to automatically create the content.


### Creating JSON files

Run `scripts/create-json.py` to create JSON files based on the `INPUT_FILEPATH` variable defined in the script.


### Creating GitHub issues

The example below will create 10 issues from the CDMS specifications Excel sheet in the `temp-repo` repository where the Number column is like `4*`

`$ scripts/create-issue.py --username opencdms --repo temp-repo --issue-limit 10 --required-title-prefix 4`

