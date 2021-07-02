Basically, what we are doing here is that we are createing a Google Drive App for our own use. As far as I know, there is no such way that we just enable API access for our Google Drive and then, use some OAuth token to make APIs calls.

### Google Drive API Relationship Diagram
![This diagram shows the relationship between your Google Drive app, Google Drive, and Google Drive API](google_drive_api_relationship_diagram.png?raw=true "Title")

### Creat a Google developer project and Enable Google Drive API for it
Refer https://developers.google.com/identity/protocols/oauth2/web-server#enable-apis

To interact with Google Drive API, you need to enable the Drive API service for your app.
To enable the Drive API, complete these steps:
- [Open the API Library](https://console.developers.google.com/apis/library) in the Google API Console.
- If prompted, select a project, or create a new one.
- The API Library lists all available APIs, grouped by product family and popularity. If the API you want to enable isn't visible in the list, use search to find it, or click View All in the product family it belongs to.
- Select **Google Drive API** under **Google Workspace**, then click the Enable button.
- If prompted, enable billing. (No worries. You will not be charged.)
- If prompted, read and accept the API's Terms of Service.

### Create authorization credentials
We use OAuth 2.0. So please refer to [Authorizing requests with OAuth 2.0](https://developers.google.com/drive/api/v3/about-auth#OAuth2Authorizing).

Any application that uses OAuth 2.0 to access Google APIs must have authorization credentials that identify the application to Google's OAuth 2.0 server. 
The following steps explain how to create credentials for your project.

First, we need to configure the **OAuth consent screen** first.

Here are the steps:
- Go to [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) page.
- Configure Consent Screen
    - Choose `External` as User Type.
    - Click `CREATE` button.
    - Just fill up the form on the next page. You can safely ignore the `App domain` and `Autorised domains` sections.
    - Click `SAVE AND CONTINUE` button.
- Select Scopes
    - Click `ADD OR REMOVE SCOPES` button.
    - Browse the list displayed and choose "`https://www.googleapis.com/auth/drive`".
    - Click `UPDATE` button.
    - Click `SAVE AND CONTINUE` button.
- Add test users
    - Click `ADD USERS` button.
    - Type your Gmail address.
    - Click `ADD` button.
    - Click `SAVE AND CONTINUE` button.
- Review Summary
    - Click `BACK TO DASHBOARD`

> - Although this gives full access to your Google Drive files, don't worry as you, yourself, will be the sole user.
>
> - Besides, you don't have to get your Google Drive App approved by Google, as we can use **test user** feature to use the app.

Second, we need to create **OAuth credentials** for the Google Duplicate Remover code to use.

Your applications can then use the credentials to access APIs that you have enabled for that project.
- Go to the [Credentials page](https://console.developers.google.com/apis/credentials).
- Click **+CREATE CREDENTIALs > OAuth client ID** in the top bar.
- Select the `Web application` as application type.
- Fill in rest of the form and click `CREATE` button.
- Click `OK` in the pop up.

Now, we need to download/save the credentials for the Google Duplicate Remover.
- On the same page, under **OAuth 2.0 Client IDs** section, find the OAuth client you just created.
- Click the download/save arrow icon.
- Save the credential file as `credentials.json`.

You are done!


