# Introduction
Performance tests based on [locust.io](https://docs.locust.io/en/stable/) tool.
Purpose - verify system stability under load/stress.

## Installation process
1. Install at least Python 3.8
2. Install docker and docker-compose
3. Clone project
4. Switch to project root
5. Create virtualenv `virtualenv --python=<path to python> venv`
6. Activate virtualenv `. venv/bin/activate`
7. Install requirements run `pip install -r requirements.txt` from root directory
8. Install custom package for sending metrics to the grafana, execute from root directory `python -m pip install .`

## Pycharm Example
<p>To debug in Pycharm you need to enable Gevent Compatible setting in File-> Settings-> Build,Execution,Deployment-> Python Debugger.</p>
<p>Note: with gevent compatible setting enabled some Flask/Django apps may not work</p>

# Build and Test
## Local test with docker-compose
1. Use `docker-compose.yml` file and set system variables:
    - BASE_URL
    - INFLUXDB_HOST
    - WAIT_TIME_MIN
    - WAIT_TIME_MAX
2. Run docker-compose `docker-compose up --build` test will start in headless mod.
3. Open a web browser and enter the following in the URL field `localhost:3000` then login using the data from the `docker-compose` file.
   Configure Grafana:
   - Go to the setting and choose data source `http://Influxdb:8086`
   - Enter the name of the database `db_locust` and check the connection `Save and test`.
   - Import `locust` dashboard, click on the `+` at the right top corner.
   - Click on `Upload dashboard JSON file` and choose `Locust_dashboard.json` located in the project root.
4. After the test is complete, run `docker-compose down` to stop docker containers, the test report will be stored in the `./reports` directory.

##.env_example
```bash
LOCUSTFILE=src/locustfiles/locustfile.py
BASE_URL=str<base_url>
WAIT_TIME_MIN=str<minimum_wait_time_between_user_tasks>
WAIT_TIME_MAX=str<maximum_wait_time_between_user_tasks>
INFLUXDB_HOST=str<host_ip_with_influxdb>
```