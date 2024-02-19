import re
from src.locustfiles.tasksets.base import BaseTaskSet


class Actions(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def main_page(self):
        with self.client.get('/', catch_response=True,
                             name=self.parent.conf.base_url) as mp_response:
            self.validate_response(response=mp_response)
            doc_url = re.findall('href="(.*?)/installation.html">documentation', mp_response.text)[0]
        return doc_url

    def documentation(self, doc_url: str):
        with self.client.get(doc_url, catch_response=True,
                             name=doc_url) as response:
            self.validate_response(response=response)

    def about(self, doc_url: str):
        with self.client.get(f'{doc_url}/what-is-locust.html',
                             catch_response=True,
                             name='/what-is-locust.html') as response:
            self.validate_response(response=response)

    def installation(self, doc_url: str):
        with self.client.get(f'{doc_url}/installation.html', catch_response=True,
                             name='/installation.html') as response:
            self.validate_response(response=response)

    def first_locustfile(self, doc_url: str):
        with self.client.get(f'{doc_url}/quickstart.html', catch_response=True,
                             name='/quickstart.html') as response:
            self.validate_response(response=response)
