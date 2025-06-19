import json
import os
import pytest
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import logging
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

@pytest.fixture(scope="class")
def get_data_api():
    api_data = {}
    load_dotenv()
    username = os.getenv("GMAIL")
    api_token = os.getenv("TOKEN_JIRA")
    LOGGER.debug(username)
    auth = HTTPBasicAuth(username, api_token)
    url_base = os.getenv("URL_BASE")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    get_headers = {
        "Accept": "application/json"
    }
    api_data["headers"] = headers
    api_data["get_headers"] = get_headers
    api_data["url_base"] = url_base
    api_data["auth"] = auth
    return api_data

@pytest.fixture
def create_issue(get_data_api):
    LOGGER.info("Create issue fixture")
    # body
    issue_body = {
        "fields": {
            "issuetype": {
                "id": "10001"
            },
            "project": {
                "id": "10000"
            },
            "summary": "Epic issue from fixture"
        },
        "update": {}
    }
    # call endpoint using requests
    response = requests.post(
        url=f"{get_data_api["url_base"]}issue",
        json=issue_body,
        headers=get_data_api["headers"],
        auth=get_data_api["auth"]
    )
    LOGGER.debug(json.dumps(response.json(), indent=4))
    # get issue id
    issue_id = response.json()["id"]
    return issue_id

@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test '{request.node.name}'")
    def end():
        LOGGER.info(f"End test '{request.node.name}'")
    request.addfinalizer(end)
