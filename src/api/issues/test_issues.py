import json
import logging
import pytest
import requests

from faker import Faker
from config.config import url_base, headers, auth, get_headers, params
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from src.api.conftest import create_project
from utils.influxdb_connection import InfluxDBConnection
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestIssues:
    @classmethod
    def setup_class(cls):
        """
        Setup before running tests
        """
        # Arrange
        cls.issue_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()
        cls.influxdb_client = InfluxDBConnection()

    def setup_method(self):
        self.response = None

    def teardown_method(self):
        self.influxdb_client.store_data_influxdb(self.response, "issues")

    @pytest.mark.acceptance
    def test_create_issue(self, test_log_name):
        """
        Test for issue creation with a project id
        :param test_log_name: (str) log test name
        """
        # body to create an issue
        issue_body = {
            "fields": {
                "issuetype": {
                    "id": "10034"
                },
                "project": {
                    "id": "10033"
                },
                "summary": f"Task {self.faker.company()}"
            },
            "update": {}
        }
        # call endpoint using rest client
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue",
            body=issue_body,
            headers=headers,
            auth=auth
        )
        self.issue_list.append(self.response["body"]["id"])
        # Assertion
        self.validate.validate_response(self.response, "create_issue")

    @pytest.mark.acceptance
    def test_get_issue(self, create_issue, test_log_name):
        """
        Test to get an issue by its id
        :param create_issue: (str) id of an issue
        :param test_log_name: (str) log test name
        """
        # call GET endpoint using rest client
        self.response = self.rest_client.send_request(
            "GET",
            url=f"{url_base}issue/{create_issue}",
            headers=get_headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "get_issue")

    @pytest.mark.acceptance
    def test_update_issue(self, create_issue, test_log_name):
        """
        Test for issue update
        :param create_issue: (str) id of an issue
        :param test_log_name: (str) log test name
        """
        # body to update issue
        update_issue_body = {
            "fields": {
                "summary": "Updated Task issue"
            },
            "update": {}
        }
        # call PUT endpoint using rest client
        self.response = self.rest_client.send_request(
            "PUT",
            url=f"{url_base}issue/{create_issue}",
            body=update_issue_body,
            headers=headers,
            auth=auth,
            params=params
        )
        # Assertion
        self.validate.validate_response(self.response, "update_issue")

    @pytest.mark.acceptance
    def test_delete_issue(self, create_issue, test_log_name):
        """
        Test issue deletion
        :param create_issue: (str) id of an issue
        :param test_log_name: (str) log test name
        """
        # call DELETE endpoint using rest client
        self.response = self.rest_client.send_request(
            "DELETE",
            url=f"{url_base}issue/{create_issue}",
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "delete_issue")

    @pytest.mark.functional
    def test_create_issue_without_body(self, test_log_name):
        """
        Test for create issue without body
        :param test_log_name: (str) log test name
        """
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue",
            headers=headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "create_issue_without_body")

    @pytest.mark.functional
    @pytest.mark.parametrize("issue_summary_test", ["123456789", "∀∁∂∃∄∅∆∇∈∉", "<script>alert('test');</script>"])
    def test_create_issue_using_different_summary_data(self, test_log_name, issue_summary_test):
        """
        Test for issue creation with different data types for the summary
        :param test_log_name: (str) log test name
        """
        # body to create an issue
        issue_body = {
            "fields": {
                "issuetype": {
                    "id": "10034"
                },
                "project": {
                    "id": f"10033"
                },
                "summary": f"{issue_summary_test}"
            },
            "update": {}
        }
        # call endpoint using rest client
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue",
            body=issue_body,
            headers=headers,
            auth=auth
        )
        self.issue_list.append(self.response["body"]["id"])
        # Assertion
        self.validate.validate_response(self.response, "create_issue")

    @pytest.mark.functional
    def test_get_issue_with_incorrect_issue_id(self, test_log_name):
        """
        Test to get an issue with an incorrect id
        :param test_log_name: (str) log test name
        """
        # call GET endpoint using requests
        self.response = self.rest_client.send_request(
            "GET",
            url=f"{url_base}issue/00000",
            headers=get_headers,
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "get_issue_with_incorrect_id")

    @pytest.mark.functional
    def test_create_issue_without_auth(self, test_log_name):
        """
        Test for create issue without auth
        :param test_log_name: (str) log test name
        """
        # body to create an issue
        issue_body = {
            "fields": {
                "issuetype": {
                    "id": "10034"
                },
                "project": {
                    "id": f"10033"
                },
                "summary": f"Task {self.faker.company()}"
            },
            "update": {}
        }
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue",
            body=issue_body,
            headers=headers
        )
        # Assertion
        self.validate.validate_response(self.response, "create_issue_without_auth")

    @pytest.mark.functional
    def test_create_issue_with_project_id(self, test_log_name, create_project):
        """
        Test for issue creation with project id
        :param test_log_name: (str) log test name
        """
        # body to create an issue
        issue_body = {
            "fields": {
                "issuetype": {
                    "id": "10034"
                },
                "project": {
                    "id": f"{create_project}"
                },
                "summary": f"Issue {self.faker.company()}"
            },
            "update": {}
        }
        # call endpoint using rest client
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue",
            body=issue_body,
            headers=headers,
            auth=auth
        )
        # self.issue_list.append(response["body"]["id"])
        # Assertion
        self.validate.validate_response(self.response, "create_issue")

    @classmethod
    def teardown_class(cls):
        """
        Clean up all issues after running tests
        """
        # Cleanup issues
        LOGGER.info("Test Issue teardown class")
        for issue_id in cls.issue_list:
            response = requests.delete(
                url=f"{url_base}issue/{issue_id}",
                auth=auth
            )
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 204:
                LOGGER.debug("Issue deleted")
