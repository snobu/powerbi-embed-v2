## Power BI Premium Embedding (aka Power BI Embedded v2) Demo

This demonstrates the **[App Owns Data](https://powerbi.microsoft.com/en-us/documentation/powerbi-developer-embed-sample-app-owns-data/)** (3rd party embedding) approach.

Demo uses the [Power BI Sample Procurement Analysis](https://powerbi.microsoft.com/en-us/documentation/powerbi-sample-procurement-analysis-take-a-tour/)  report from the Power BI sample gallery (_Get data_).<br>
Publish to **App Workspace**, not _My Workspace_, this is important. It should be the only report in your App Workspace, otherwise you'll need to change the backend to return its index from the result array.

Material Design controls borrowed from [Creative Tim](https://www.creative-tim.com/product/material-kit).<br>
TODO: Swap Material Design for [Fluent Design System](https://fluent.microsoft.com) (Project Neon).

![Screenshot](screenshot.png)

You can test drive the demo here: http://powerbi-static-frontend.azurewebsites.net/

Original contributors (Microsoft):
- Andrey Vykhodtsev - https://github.com/vykhand
- Adrian Calinescu - https://github.com/snobu

Pull Requests are more than welcome.

### Legend

**backend-as-func**<br>
C# HTTP Trigger Azure Function acting as backend (returns embed token).

*Needs some hacking as it can only handle 1st report in a given workspace by ID*

**root dir**<br>
A Flask application containing both frontend and backend (in Python this time):
- Copy `config.template.yml` to `config.yml` and add your secrets
- to run app locally with Flask, just run `python app.py`
- to run your app locally as a docker container, run `python util.py run_docker`
- To publish your app to Azure App Service (linux Web App as docker container), run `python util.py create_app` or `python util.py create_app --dry` to just print the commands
- to delete your app, run `python util.py delete_app`

![Oauth Dance Gif](oauth-dance.gif)
Last frame of this GIF is conviniently provided [as PNG](oauth-dance.png).

Slide borrowed from this highly recommended video on v2 embedding -

[![Hangouts Video](https://img.youtube.com/vi/xKTPI2pEl9I/0.jpg)](https://www.youtube.com/watch?v=xKTPI2pEl9I)


**What's new 20.09.2017**

 *	Configuration is done via yaml file config.yml. It must be copied from config.template.yml. `config.yml` is ignored by git and docker
 *	Configuration takes report name and
 *	Added some python scripts to automate tasks, see util.py
 *	Run docker locally `python util.py run_docker`
 *	Set env variables from yaml file `python util.py setenv`
 *	Create web app `python util.py create_app [-d|--dry]`
 *	Delete web app `python util.py delete_app`

