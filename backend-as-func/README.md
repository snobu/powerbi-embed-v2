### Wait, where do i get that Workspace ID from?

1. Login to https://app.powerbi.com with your PowerBIMaster account (that has the Premium subscription).
2. Go to **Workspaces -> App Workspaces** and pick the App Workspace you'll deploy the sample report to.
3. The Workspace is the GUID after `/groups/`<br>
   (i.e. `https://app.powerbi.com/groups/c692d43d-xxxx-xxxx-xxxx-xxxxxxxxxxxx/contentlist`)


Your Function App's _Application Settings_ need to contain the following values.

| Settings Key | Settings Value                                     |
| ------------ | -------------------------------------------------- |
| pbiUsername  | YourPowerBIMasterUser@YourTenant.onmicrosoft.com   |
| pbiPassword  | PasSSw0Rd@123OfCourse                              |
| authorityUrl | https://login.windows.net/common/oauth2/authorize/ |
| resourceUrl  | https://analysis.windows.net/powerbi/api           |
| clientId     | GUID-OF-AZUREAD-NATIVE-APP                         |
| apiUrl       | https://api.powerbi.com                            |
| groupId      | GUID-OF-POWERBI-WORKSPACE-SEE-README-NOTES         |

### Usage

#### Ordinary Call

A call to the Function App without any parameters will try to find a best fit for the report ID. The function will retriev all reports from the report group specified by the `GroupId` and then take the first available report ID.

#### Call with Request Params

In case you want to specify the report ID to create the token for, you can hand over a query parameter `reportId` like in the following URL<br>
   `https://<FUNCTION APP>.azurewebsites.net/api/<FUNCTION NAME>?code=SV...kaw==&reportId=01dbe35b-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Notes

- Authentication is only possible against a registered app in Azure, which is of the Application Type **Native**.<br>
  If you haven't registered your application, you can do this at https://dev.powerbi.com/apps.
- Granting permissions is needed in order to have the Function App access the registered app<br>
  1. In Azure go to **App Registrations** and select the registered app of the application type **Native**<br>
  2. In the **API ACCESS**-section go to **Required permissions** and execute **Grant Permissions**
