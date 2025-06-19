import json
import logging
import requests
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestIssues:
    def test_create_issue(self, get_data_api, test_log_name):
        issue_body = {
            "fields": {
                "issuetype": {
                    "id": "10001"
                },
                "project": {
                    "id": "10000"
                },
                "summary": "Epic issue from test"
            },
            "update": {}
        }
        response = requests.post(
            url=f"{get_data_api["url_base"]}issue",
            json=issue_body,
            headers=get_data_api["headers"],
            auth=get_data_api["auth"]
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 201

    def test_get_issue(self, get_data_api, create_issue, test_log_name):
        # call endpoint
        response = requests.get(
            url=f"{get_data_api["url_base"]}issue/{create_issue}",
            headers=get_data_api["get_headers"],
            auth=get_data_api["auth"]
        )
        LOGGER.debug("Response: %s", json.dumps(response.json(), indent=4))
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 200

    def test_update_issue(self, get_data_api, create_issue, test_log_name):
        update_issue_body = {
            "fields": {
                "summary": "Updated Epic issue"
            },
            "update": {}
        }
        response = requests.put(
            url=f"{get_data_api["url_base"]}issue/{create_issue}",
            json=update_issue_body,
            headers=get_data_api["headers"],
            auth=get_data_api["auth"]
        )
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 204

    def test_delete_issue(self, get_data_api, create_issue, test_log_name):
        response = requests.delete(
            url=f"{get_data_api["url_base"]}issue/{create_issue}",
            auth=get_data_api["auth"]
        )
        LOGGER.debug("Status Code: %s", str(response.status_code))
        assert response.status_code == 204
