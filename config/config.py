import os

from pathlib import Path
from dotenv import dotenv_values


class Config:

    def __init__(self, env_file: str = '.env'):
        path = Path(__file__).parent.parent / env_file
        config = dotenv_values(path)
        url = config.get('BASE_URL', os.getenv('BASE_URL'))
        self.base_url = f'http://{url}'
        self.wait_time_min = float(config.get('WAIT_TIME_MIN', os.getenv('WAIT_TIME_MIN')))
        self.wait_time_max = float(config.get('WAIT_TIME_MAX', os.getenv('WAIT_TIME_MAX')))
        self.influxdb_host = config.get('INFLUXDB_HOST', os.getenv('INFLUXDB_HOST'))
        self.job_url = f'http://jobs.{url}'
