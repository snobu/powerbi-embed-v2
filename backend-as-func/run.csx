using System.Net;
using System.Configuration;
using Microsoft.PowerBI.Api.V2;
using Microsoft.PowerBI.Api.V2.Models;
using Microsoft.IdentityModel.Clients.ActiveDirectory;
using Microsoft.Rest;

private static readonly string Username = ConfigurationManager.AppSettings["pbiUsername"];
private static readonly string Password = ConfigurationManager.AppSettings["pbiPassword"];
private static readonly string AuthorityUrl = ConfigurationManager.AppSettings["authorityUrl"];
private static readonly string ResourceUrl = ConfigurationManager.AppSettings["resourceUrl"];
private static readonly string ClientId = ConfigurationManager.AppSettings["clientId"];
private static readonly string ApiUrl = ConfigurationManager.AppSettings["apiUrl"];
private static readonly string GroupId = ConfigurationManager.AppSettings["groupId"];

public static async Task<HttpResponseMessage> Run(HttpRequestMessage req, TraceWriter log)
{
	HttpResponseMessage response;

	log.Info("C# HTTP trigger function processed a request.");

	// Read reportId from query params
	string reportId = req.GetQueryNameValuePairs()
		.FirstOrDefault(q => string.Compare(q.Key, "reportId", true) == 0)
		.Value;

	if (reportId != null)
	{
		log.Info($"Report ID from Query Params: {reportId}");
	}

	// Create a user password cradentials.
	var credential = new UserPasswordCredential(Username, Password);

	// Authenticate using created credentials
	var authenticationContext = new AuthenticationContext(AuthorityUrl);
	var authenticationResult = await authenticationContext.AcquireTokenAsync(ResourceUrl, ClientId, credential);
	log.Info($"We have a Bearer token: {authenticationResult.AccessToken.Substring(0, 9)}"); 

	if (authenticationResult == null)
	{
		log.Error("Authentication Failed, authenticationResult is null.");
	}

	var tokenCredentials = new TokenCredentials(authenticationResult.AccessToken, "Bearer");

	// Create a Power BI Client object. It will be used to call Power BI APIs.
	using (var client = new PowerBIClient(new Uri(ApiUrl), tokenCredentials))
	{
		// Generate Embed Configuration.
		var embedConfig = new EmbedConfig();

		if (reportId != null)
		{
			// Get a list of reports from the Group and search for the specific Report ID
			var reports = await client.Reports.GetReportsInGroupAsync(GroupId);
			var report = reports.Value.FirstOrDefault(q => string.Compare(q.Id, reportId, true) == 0);

			if (report == null)
			{
				log.Error($"Can't find report for Report ID {reportId} from the request parameters.");
			}
			else
			{
				embedConfig.reportId = report.Id;
				embedConfig.embedUrl = report.EmbedUrl;
			}
		}
		else {
			// Trying to find a default reportId

			// Get a list of reports.
			var reports = await client.Reports.GetReportsInGroupAsync(GroupId);

			// Pick 1st report in group (also known as workspace)
			var report = reports.Value.FirstOrDefault();

			// OR Pick the 3rd report in group (also known as workspace)
			// var report = reports.Value.Skip(2).First();

			if (report == null)
			{
				log.Error($"Can't find report for Group ID {GroupId}");
			}
			else
			{
				embedConfig.reportId = report.Id;
				embedConfig.embedUrl = report.EmbedUrl;
			}
		}

		// Generate Embed Token.
		var generateTokenRequestParameters = new GenerateTokenRequest(accessLevel: "view");
		var tokenResponse = await client.Reports.GenerateTokenInGroupAsync(GroupId, embedConfig.reportId, generateTokenRequestParameters);

		if (tokenResponse == null)
		{
			log.Error("Failed to generate embed token.");
		}
		else
		{
			embedConfig.embedToken = tokenResponse.Token;
		}

		response = (embedConfig != null) ?
			req.CreateResponse(HttpStatusCode.OK, embedConfig) :
			req.CreateResponse(HttpStatusCode.InternalServerError, "Things have gone horribly wrong.");
	}

	return response;
}

public class EmbedConfig
{
	public string embedToken { get; set; }
	public string embedUrl { get; set; }
	public string reportId { get; set; }
}
