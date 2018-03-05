import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from apiclient.errors import HttpError

flags = None


class DriveStorage(object):
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'

    def _get_credentials(self,):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    def __init__(self,):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        self.file_service = service.files()
        self.perm_service = service.permissions()

    def write(self, filename):
        media = MediaFileUpload(filename=filename, mimetype=None, chunksize=1024, resumable=True)
        file_metadata = {'name': filename}

        self.file_service.create(body=file_metadata, media_body=media).execute()
        return f

    def _isExists(self, fileid):
        try:
            mdata = self.file_service.get(fileId=fileid).execute()
        except HttpError:
            return False
        return True

    def read(self, fileid):
        if self._isExists(fileid):
            data = self.file_service.get_media(fileId=fileid).execute()
            print(data)
        else:
            print("File Unavailable")

    def search(self, name_subs):
        query = "name contains '{}'".format(name_subs)
        response = self.file_service.list(q=query, pageSize=5).execute()
        items = response.get('files', [])
        if not items:
            print("No such item found")

        for f in items:
            print("{name}\t{id}".format(name=f['name'], id=f['id']))

    def delete(self, fileid):
        if not self._isExists(fileid):
            print('File already non-existant')
            return None

        self.file_service.delete(fileId=fileid).execute()


    def add_permissions_user(self, fileid, email, role):
        if not self._isExists(fileid):
            print("No such file exists.")
            return None
        permission = {'type': 'user', 'role': role, 'emailAddress': email}
        self.perm_service.create(fileId=fileid, body=permission).execute()
