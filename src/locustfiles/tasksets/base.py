import logging

from locust import SequentialTaskSet


class BaseTaskSet(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.success_status_codes = (200, 201, 204, 300, 301, 302, 304)

    def validate_response(self, response):
        if response.status_code in self.success_status_codes:
            response.success()
        else:
            response.failure(response.status_code)
            logging.error(
                f'error occurred: {response.request_meta["request_type"]}, '
                f'path {response.request_meta["name"]}, '
                f'response status {response.status_code}, '
                f'response content {response.content}'
            )
