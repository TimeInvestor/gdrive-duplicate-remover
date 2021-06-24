# Google Drive Duplicate Files Remover
Google Drive Duplicate Files Remover is a tool for searching, finding and removing duplicate files in your Google Drive.

## Privacy & Data Safety
Your data is totally safe because
 - the program uses your own Google Drive App and your own Google account authentication. 
 - it only reads and changes files metadata. No file content reading, exporting, downloading or deletion. 
 - it uses soft deletion which means it trashes duplicate files instead of deleting them permanently.

> Note:
>  - If you need to delete the trashed files and release Google Drive space immediately, login to your Google Drive, go to `Bin`, and delete selected files or empty entire bin.
>  - You need to refresh the browser page to see any change in Google Drive storage space.

## Prerequisite: Google Account Setup
Basically, what we are doing here is that we are createing a Google Drive App for our own use.
As far as I know, there is no such way that we just enable API access for our Google Drive and then, use some OAuth token to make APIs calls.

### Google Drive API Relationship Diagram
![This diagram shows the relationship between your Google Drive app, Google Drive, and Google Drive API](resources/google_drive_api_relationship_diagram.png?raw=true "Title")

### Creat a Google developer project and Enable Google Drive API for it
Refer https://developers.google.com/drive/api/v3/enable-drive-api

### Set up authentication
Refer https://developers.google.com/drive/api/v3/about-auth

## Prerequisite: Program Execution Environment
Before you begin, ensure you have met the following requirements:
* Python 3.6 or higher version.

## Installing Google Drive Duplicate Files Remover
To install Google Drive Duplicate Files Remover, follow these steps:

**Download code**
```shell
git clone git@github.com:TimeInvestor/gdrive-duplicate-remover.git
```
**Install required Python libraries**
```shell
pip install google-api-python-client
```

## Using Google Drive Duplicate Files Remover

To use Google Drive Duplicate Files Remover, follow these steps:

```shell
# Go to code folder
cd <path to gdrive-duplicate-remover>
# Run the main script
python main.py
```

## Contributing to Google Drive Duplicate Files Remover
<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->
To contribute to Google Drive Duplicate Files Remover, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin gdrive-duplicate-remover/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me you can reach me at zhenglisheng@gmail.com.

## License
This project uses the following license: [MIT License](LICENSE).
