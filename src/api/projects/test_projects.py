import json
import logging
import pytest
import requests

from faker import Faker
from config.config import url_base, headers, auth, get_headers, account_id
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.influxdb_connection import InfluxDBConnection
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
        cls.influxdb_client = InfluxDBConnection()

    def setup_method(self):
        self.response = None

    def teardown_method(self):
        self.influxdb_client.store_data_influxdb(self.response, "projects")

    @pytest.mark.acceptance
    def test_create_project(self, test_log_name):
        """
        Test for project creation
        :param test_log_name: (str) log test name
        """
        # body to create a project
        project_body = {
            "key": f"A{self.faker.currency_code()}",
            "name": f"Project {self.faker.aba()}",
            "leadAccountId": f"{account_id}",
            "projectTypeKey": "business"
        }
        # call endpoint using rest client
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}project",
            body=project_body,
            headers=headers,
            auth=auth
        )
        self.projects_list.append(self.response["body"]["id"])
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "create_project")

    @pytest.mark.acceptance
    def test_get_project(self, create_project, test_log_name):
        """
        Test to get a project by its id
        :param create_project: (str) id of a project
        :param test_log_name: (str) log test name
        """
        # call GET endpoint using rest client
        self.response = self.rest_client.send_request(
            "GET",
            url=f"{url_base}project/{create_project}",
            headers=get_headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "get_project")

    @pytest.mark.acceptance
    def test_update_project(self, create_project, test_log_name):
        """
        Test for project update
        :param create_project: (str) id of a project
        :param test_log_name: (str) log test name
        """
        # body to update project
        update_project_body = {
            "description": "Update project test API",
            "name": f"Project {create_project} (update test)"
        }
        # call PUT endpoint using rest client
        self.response = self.rest_client.send_request(
            "PUT",
            url=f"{url_base}project/{create_project}",
            body=update_project_body,
            headers=headers,
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "update_project")

    @pytest.mark.acceptance
    def test_delete_project(self, create_project, test_log_name):
        """
        Test project deletion
        :param create_project: (str) id of a project
        :param test_log_name: (str) log test name
        """
        # call DELETE endpoint using rest client
        self.response = self.rest_client.send_request(
            "DELETE",
            url=f"{url_base}project/{create_project}",
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "delete_project")

    @pytest.mark.functional
    def test_create_project_without_body(self, test_log_name):
        """
        Test for create project without body
        :param test_log_name: (str) log test name
        """
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}project",
            headers=headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "create_project_without_body")

    @classmethod
    def teardown_class(cls):
        """
        Clean up all projects after running tests
        """
        # Cleanup projects
        LOGGER.info("Test Project teardown class")
        for project_id in cls.projects_list:
            response = requests.delete(
                url=f"{url_base}project/{project_id}",
                auth=auth
            )
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 204:
                LOGGER.debug("Project deleted")