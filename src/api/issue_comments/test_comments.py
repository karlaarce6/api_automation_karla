import json
import logging
import pytest
import requests

from faker import Faker
from config.config import url_base, headers, auth, get_headers
from helper.rest_client import RestClient
from helper.validate_response import ValidateResponse
from utils.influxdb_connection import InfluxDBConnection
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestIssueComments:
    @classmethod
    def setup_class(cls):
        """
        Setup before running tests
        """
        # Arrange
        cls.comments_list = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.faker = Faker()
        cls.influxdb_client = InfluxDBConnection()

    def setup_method(self):
        self.response = None

    def teardown_method(self):
        self.influxdb_client.store_data_influxdb(self.response, "comments")

    @pytest.mark.acceptance
    def test_add_comment(self, test_log_name):
        """
        Test for adding a comment to an issue
        :param test_log_name: (str) log test name
        """
        # body to create a comment
        comment_body = {
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "text": f"{self.faker.sentence()}",
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
        # call endpoint using rest client
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue/EXU-1/comment",
            body=comment_body,
            headers=headers,
            auth=auth
        )
        self.comments_list.append(self.response["body"]["id"])
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "add_comment")

    @pytest.mark.acceptance
    def test_get_comment(self, add_comment, test_log_name, create_issue):
        """
        Test to get a comment by its id
        :param add_comment: (str) id of a comment
        :param test_log_name: (str) log test name
        """
        # call GET endpoint using requests
        self.response = self.rest_client.send_request(
            "GET",
            url=f"{url_base}issue/{create_issue}/comment/{add_comment}",
            headers=get_headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "get_comment")

    @pytest.mark.acceptance
    def test_update_comment(self, add_comment, test_log_name, create_issue):
        """
        Test for comment update
        :param add_comment: (str) id of a comment
        :param test_log_name: (str) log test name
        """
        # body to update comment
        update_comment_body = {
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "text": "Update comment test",
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
        # call PUT endpoint using rest client
        self.response = self.rest_client.send_request(
            "PUT",
            url=f"{url_base}issue/{create_issue}/comment/{add_comment}",
            body=update_comment_body,
            headers=headers,
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "update_comment")

    @pytest.mark.acceptance
    def test_delete_comment(self, add_comment, test_log_name, create_issue):
        """
        Test comment deletion
        :param add_comment: (str) id of a comment
        :param test_log_name: (str) log test name
        """
        # call DELETE endpoint using rest client
        self.response = self.rest_client.send_request(
            "DELETE",
            url=f"{url_base}issue/{create_issue}/comment/{add_comment}",
            auth=auth
        )
        # Assertion
        self.validate.validate_response(self.response, "delete_comment")

    @pytest.mark.functional
    def test_add_comment_without_body(self, test_log_name):
        """
        Test for add comment without body
        :param test_log_name: (str) log test name
        """
        self.response = self.rest_client.send_request(
            "POST",
            url=f"{url_base}issue/EXU-1/comment",
            headers=headers,
            auth=auth
        )
        LOGGER.debug("Response: %s", json.dumps(self.response["body"], indent=4))
        # Assertion
        self.validate.validate_response(self.response, "add_comment_without_body")

    @classmethod
    def teardown_class(cls):
        """
        Clean up all comments after running tests
        """
        # Cleanup comments
        LOGGER.info("Test Comments teardown class")
        for comment_id in cls.comments_list:
            response = requests.delete(
                url=f"{url_base}issue/EXU-1/comment/{comment_id}",
                auth=auth
            )
            LOGGER.debug("Status Code: %s", str(response.status_code))
            if response.status_code == 204:
                LOGGER.debug("Comment deleted")
