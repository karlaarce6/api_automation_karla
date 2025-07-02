import requests
import logging
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class RestClient:
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method_name, url, auth=None, headers=None, body=None, params=None):
        response_updated = {}
        methods = {
            "GET": self.session.get,
            "POST": self.session.post,
            "PUT": self.session.put,
            "DELETE": self.session.delete
        }

        try:
            response = methods[method_name](url=url, auth=auth, headers=headers, json=body, params=params)
            response.raise_for_status()
            response_updated["body"] = (
                response.json() if response.text else {"message": "No body content"}
            )
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)
            LOGGER.debug(response_updated)

        except requests.exceptions.HTTPError as e:
            LOGGER.error("HTTP Error: %s", e)
            response_updated["body"] = (
                response.json() if response.text else {"message": "HTTP Error"}
            )
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = dict(response.headers)

        except requests.exceptions.ConnectionError as e:
            LOGGER.error("Connection Error: %s", e)
            response_updated["body"] = (
                response.json() if response.text else {"message": "Connection Error"}
            )
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}

        except requests.exceptions.RequestException as e:
            LOGGER.error("Request Exception: %s", e)
            response_updated["body"] = (
                response.json() if response.text else {"message": "Request Failed"}
            )
            response_updated["status_code"] = response.status_code
            response_updated["headers"] = {}

        return response_updated
