import json
import logging

import jsonschema

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class ValidateResponse:
    def validate_response(self, actual_response, file_name):
        expected_response = self.read_input_data(f"C:/Users/Karla.Arce/PycharmProjects/JiraAPI/src/api/input_json/{file_name}.json")
        self.validate_value(actual_response["body"], expected_response["body"], "body")
        self.validate_value(actual_response["status_code"], expected_response["status_code"], "status_code")
        self.validate_value(actual_response["headers"], expected_response["headers"], "headers")

    def validate_value(self, actual_value, expected_value, key_compare):
        if key_compare == "status_code":
            LOGGER.debug(f"Actual status code: %s", actual_value)
            LOGGER.debug(f"Expected status code: %s", expected_value)
            assert (
                actual_value == expected_value
            ), f"Expected Status Code: {expected_value} but received {actual_value}"
        elif key_compare == "headers":
            LOGGER.debug(f"Actual headers: %s", actual_value)
            LOGGER.debug(f"Expected headers: %s", expected_value)
            assert (
                expected_value.items() <= expected_value.items()
            ), f"Expected headers: {expected_value} but received {actual_value}"
        elif key_compare == "body":
            schema = False
            LOGGER.debug(f"Actual body: %s", actual_value)
            LOGGER.debug(f"Expected body: %s", expected_value)
            try:
                jsonschema.validate(instance=actual_value, schema=expected_value)
                schema = True
            except jsonschema.exceptions.ValidationError as e:
                LOGGER.debug("JSON validator error: %s", e)
            assert schema, f"Expected body: {expected_value} but received {actual_value}"

    def read_input_data(self, file_name):
        LOGGER.debug(f"Reading input data from {file_name}")
        with open(file_name, encoding="utf-8") as f:
            data = json.load(f)
        LOGGER.debug(f"Content data {data}")
        return data
