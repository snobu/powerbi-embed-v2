az webapp deployment user set --user-name <user> --password <password>
az group create --name PBIWebapp --location "West Europe"
az appservice plan create --name PBIWebappPlan --resource-group PBIWebapp --sku FREE
az webapp create --name pbiembed001 --resource-group PBIWebapp --plan PBIWebappPlan --deployment-local-git
az webapp deployment source sync --name pbiembed001 --resource-group PBIWebapp
REM az webapp config set --python-version 3.4 --name pbiembed001 --resource-group PBIWebapp

REM az webapp delete -n pbiembed001 -g PBIWebapp
D:\home\python361x64\python.exe -m pip install --upgrade -r _requirements.txt
