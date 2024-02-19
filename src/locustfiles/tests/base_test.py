from src.locustfiles.tasksets.base import BaseTaskSet


class TestBase(BaseTaskSet):

    def __init__(self, parent):
        super().__init__(parent)

    def on_start(self):
        super().on_start()
