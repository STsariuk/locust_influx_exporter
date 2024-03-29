from locust.env import Environment
from locust import HttpUser, between

from config.config import Config

from src.locustfiles.tests.visitor import SiteVisitor
from locust_influx import expose_metrics

expose_metrics(interval_ms=2000)


class TestExecution(HttpUser):
    conf = Config()
    wait_time = between(conf.wait_time_min, conf.wait_time_max)
    host = conf.base_url
    tasks = {SiteVisitor: 1}


if __name__ == '__main__':
    env = Environment(user_classes=[TestExecution])
    TestExecution(env).run()
