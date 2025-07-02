import json
import logging
import pytest
import requests
from faker import Faker

from config.config import url_base, headers, auth, get_headers, params, account_id
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestProjects:
    @classmethod
    def setup_class(cls):
        """
        Setup before running tests
        """
        # Arrange
        cls.projects_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()

    @pytest.mark.acceptance
    def test_create_project(self, test_log_name):
        """
        Test for project creation
        :param test_log_name: (str) log test name
        """
        # body to create an issue
        project_body = {
            "key": f"A{self.faker.currency_code()}",
            "name": f"Project {self.faker.aba()}",
            "leadAccountId": f"{account_id}",
            "projectTypeKey": "business"
        }
        # call endpoint using rest client
        response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}project",
            body=project_body,
            headers=headers,
            auth=auth
        )
        self.projects_list.append(response["body"]["id"])
        LOGGER.debug("Response: %s", json.dumps(response["body"], indent=4))
        # Assertion
        self.validate.validate_response(response, "create_project")

    @classmethod
    def teardown_class(cls):
        """
        Clean up all projects after running tests
        """
        # Cleanup issues
        LOGGER.info("Test Project teardown class")
        for project_id in cls.projects_list:
            response = requests.delete(
                url=f"{url_base}project/{project_id}",
                auth=auth
            )
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 204:
                LOGGER.debug("Project deleted")
