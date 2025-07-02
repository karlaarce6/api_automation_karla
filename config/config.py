import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
username = os.getenv("GMAIL")
api_token = os.getenv("TOKEN_JIRA")
auth = HTTPBasicAuth(username, api_token)
url_base = os.getenv("URL_BASE")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
get_headers = {
    "Accept": "application/json"
}
params = {"returnIssue": True}
web_hook = os.getenv("WEB_HOOK")
account_id = os.getenv("ACCOUNT_ID")
