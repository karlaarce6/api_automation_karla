import json
import pytest
import requests
import logging
from faker import Faker

from config.config import url_base, headers, auth, account_id
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)
faker = Faker()

# Arrange
@pytest.fixture
def test_log_name(request):
    LOGGER.info(f"Start test '{request.node.name}'")
    def end():
        LOGGER.info(f"End test '{request.node.name}'")
    request.addfinalizer(end)

@pytest.fixture
def create_project():
    LOGGER.info("Create project fixture")
    # body to create a project
    project_body = {
        "key": f"A{faker.currency_code()}",
        "name": f"Project {faker.aba()}",
        "leadAccountId": f"{account_id}",
        "projectTypeKey": "business"
    }
    # call endpoint using requests
    response = requests.post(
        url=f"{url_base}project",
        json=project_body,
        headers=headers,
        auth=auth
    )
    LOGGER.debug(json.dumps(response.json(), indent=4))
    # get project id
    project_id = response.json()["id"]
    yield project_id
    delete_project(project_id)

# Arrange
@pytest.fixture
def create_issue(create_project):
    LOGGER.info("Create issue fixture")
    # body
    issue_body = {
        "fields": {
            "issuetype": {
                "id": "10034"
            },
            "project": {
                "id": f"{create_project}"
            },
            "summary": "Task issue from fixture"
        },
        "update": {}
    }
    # call endpoint using requests
    response = requests.post(
        url=f"{url_base}issue",
        json=issue_body,
        headers=headers,
        auth=auth
    )
    LOGGER.debug(json.dumps(response.json(), indent=4))
    # get issue id
    issue_id = response.json()["id"]
    yield issue_id
    # delete_issue(issue_id)

@pytest.fixture
def add_comment(create_issue):
    LOGGER.info("Add Comment fixture")
    # body
    comment_body = {
        "body": {
            "content": [
                {
                    "content": [
                        {
                            "text": f"{faker.sentence()}",
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        }
    }
    # call endpoint using requests
    response = requests.post(
        url=f"{url_base}issue/{create_issue}/comment",
        json=comment_body,
        headers=headers,
        auth=auth
    )
    LOGGER.debug(json.dumps(response.json(), indent=4))
    # get comment id
    comment_id = response.json()["id"]
    yield comment_id
    # delete_comment(comment_id)

def delete_comment(comment_id):
    LOGGER.info("Delete comment fixture (yield)")
    response = requests.delete(
        url=f"{url_base}issue/EXU-1/comment/{comment_id}",
        auth=auth
    )
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 204:
        LOGGER.debug("Comment deleted")
    else:
        LOGGER.debug("No comment found to delete")

def delete_issue(issue_id):
    LOGGER.info("Delete issue fixture (yield)")
    response = requests.delete(
        url=f"{url_base}issue/{issue_id}",
        auth=auth
    )
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 204:
        LOGGER.debug("Issue deleted")
    else:
        LOGGER.debug("No issue found to delete")

def delete_project(project_id):
    LOGGER.info("Delete project fixture (yield)")
    response = requests.delete(
        url=f"{url_base}project/{project_id}",
        auth=auth
    )
    LOGGER.debug("Status Code: %s", str(response.status_code))
    if response.status_code == 204:
        LOGGER.debug("Project deleted")
    else:
        LOGGER.debug("No project found to delete")
