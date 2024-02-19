import requests
from locust.env import Environment
from locust import HttpUser, between, events

from config.config import Config

from src.locustfiles.tests.visitor import SiteVisitor

# @events.test_start.add_listener
# def on_test_start(environment, **_kw):
#     tmp_conf = environment.user_classes_by_name['TestExecution'].conf
#     resp = requests.get(tmp_conf.base_url)
#     csrftoken = resp.cookies['csrftoken']


class TestExecution(HttpUser):
    conf = Config()
    wait_time = between(conf.wait_time_min, conf.wait_time_max)
    host = conf.base_url
    tasks = {SiteVisitor: 1}


if __name__ == '__main__':
    env = Environment(user_classes=[TestExecution])
    TestExecution(env).run()
