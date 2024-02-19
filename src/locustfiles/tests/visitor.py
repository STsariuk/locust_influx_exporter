from locust import task

from src.locustfiles.tasksets.visitor_action import Actions


class SiteVisitor(Actions):

    def __init__(self, parent):
        super().__init__(parent)
        self.doc_url = None

    @task
    def open_main_page(self):
        self.doc_url = self.main_page()

    @task
    def open_documentations(self):
        self.documentation(doc_url=self.doc_url)

    @task
    def open_locust_about(self):
        self.about(doc_url=self.doc_url)

    @task
    def open_locust_installation(self):
        self.installation(doc_url=self.doc_url)

    @task
    def open_write_locustfile(self):
        self.first_locustfile(doc_url=self.doc_url)

    @task
    def stop(self):
        self.interrupt()
