import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gd_content import *

SCOPES = ['https://www.googleapis.com/auth/documents']
DOCUMENT_ID = '1LtpABltqtuhF-Id-hYZ9WT3anC2GVDLZodasWR8aVUA'

credentials = None
# pickle stores user's access and refresh tokens
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

# if no (valid) credentials available, let user log in
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'gd_credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
    
    # save the credentials for next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)

# build service
gd = build('docs', 'v1', credentials=credentials)

# get document
document = gd.documents().get(documentId=DOCUMENT_ID).execute()

# init document details
document_content = document.get('body').get('content')
document_text = read_structural_elements(document_content)

# populate posts
'''
Format : 
    date
    text

    tags
'''
def getPosts():
    posts = {}
    cur_date = cur_text = cur_tags = ''

    blocks = document_text.split('\n\n')
    for block in blocks:
        if not block:
            continue

        tokens = block.split('\n', 1)
        if len(tokens) == 1:
            if 'Tags' not in tokens[0]:
                continue

        if 'Tags' not in tokens[0]:
            # it is a date
            cur_date = tokens[0]
            cur_text = tokens[1]
        if 'Tags' in tokens[0]:
            # it is a tag
            cur_tags = tokens[0][6:]
            posts[cur_date] = [cur_text, cur_tags]

    return posts

def getCurPost():
    posts = getPosts()
    now = str(datetime.date.today()).split('-')
    now = [now[1], now[2], now[0]]
    if now[0][0] == '0':
        now[0] = now[0][1:]
    if now[1][0] == '0':
        now[1] = now[1][1:]
    if now[2][0:2] == '20':
        now[2] = now[2][2:]
    now = '/'.join(now)
    now = '10/16/20'
    if now in posts.keys():
        f = open('post_text.txt', 'w')
        f.write(posts[now][0])
        f.close()

        f = open('post_tags.txt', 'w')
        f.write(posts[now][1])
        f.close()
        return posts[now]

getCurPost()
