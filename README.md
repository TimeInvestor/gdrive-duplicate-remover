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

Please read [Google Account Setup](/resources/Google_Account_Setup.md) readme file for the details.

After successful setup, you will have OAuth credentials saved in a file named `credentials.json`. 
We need this file later.

## Prerequisite: Program Execution Environment
Before you begin, ensure you have met the following requirements:
* Python 3.6 or higher version.

## Installing Google Drive Duplicate Files Remover
To install Google Drive Duplicate Files Remover, follow these steps:

**Download code**
```shell
git clone git@github.com:TimeInvestor/gdrive-duplicate-remover.git
```

**(optional) Configure Python virtual environment**

If you want to use Python virtual environment for the project, please do so.
> If you want to learn more about Python virtual environment, you could refer to https://realpython.com/python-virtual-environments-a-primer/.

**Install required Python libraries**
```shell
cd gdrive-duplicate-remover
pip install google-api-python-client
```

## Configuration
We need access (OAuth 2.0) credentials for the code to call Google Drive API. 
So put your saved `credentials.json` file at the root of the project folder.

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
