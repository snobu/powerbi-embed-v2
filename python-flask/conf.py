import os
def setenv():
    os.environ["AUTHORITY"] = "https://login.microsoftonline.com/common"
    os.environ["RESOURCE"] = "https://analysis.windows.net/powerbi/api"
    os.environ["BACKEND_URL"] = "/api/token"
    os.environ["CLIENTID"] = "THE-GUID-OF-YOUR-AZUREAD-NATIVE-APP"
    os.environ["USERNAME"] = "YourPowerBIMasterUser@TenantName.onmicrosoft.com"
    os.environ["PASSWORD"] = "Password-for-YourPowerBIMasterUser"
    # if these are not set, it is going to get first workspace and first report
    #os.environ["PBI_WORKSPACE_NAME"] = "workspace 2"
    #os.environ["PBI_REPORT_NAME"] = "Retail Analysis Sample PBIX"