import gevent
import logging
import sys
import os

from datetime import datetime
from typing import Callable


from influxdb import InfluxDBClient
from locust import events

__all__ = ['expose_metrics']

log = logging.getLogger('locust_influx')

cache = []
stop_flag = False

influx_host_ip = os.getenv('INFLUXDB_HOST')
if influx_host_ip is None:
    sys.exit('INFLUXDB_HOST environment variable is not set.')


def __make_data_point(measurement: str, tags: dict, fields: dict, time: datetime):
    """
    Create a list with a single point to be saved to influxdb.

    :param measurement: The measurement where to save this point.
    :param tags: Dictionary of tags to be saved in the measurement.
    :param fields: Dictionary of field to be saved to measurement.
    :param time: The time os this point.
    """
    return {'measurement': measurement, 'tags': tags, 'time': time, 'fields': fields}


def __listen_for_requests_events(node_id, measurement: str = 'locust_requests') -> Callable:
    """
    Persist request information to influxdb.

    :param node_id: The id of the node reporting the event.
    :param measurement: The measurement where to save this point.
    """

    def event_handler(request_type=None, name=None, response=None, response_time=None, response_length=None,
                      exception=None, **_) -> None:
        time = datetime.utcnow()
        tags = {
            'node_id': node_id,
            'request_type': request_type,
            'name': name,
            'response': response.status_code,
            'exception': repr(exception),
        }
        fields = {
            'response_time': response_time,
            'response_length': response_length,
            'counter': 1
        }
        point = __make_data_point(measurement, tags, fields, time)
        cache.append(point)

    return event_handler


def __flush_points(influxdb_client: InfluxDBClient) -> None:
    """
    Write the cached data points to influxdb

    :param influxdb_client: An instance of InfluxDBClient
    :return: None
    """
    global cache
    log.debug(f'Flushing points {len(cache)}')
    to_be_flushed = cache
    cache = []
    success = influxdb_client.write_points(to_be_flushed)
    if not success:
        log.error('Failed to write points to influxdb.')
        # If failed for any reason put back into the beginning of cache
        cache.insert(0, to_be_flushed)


def __flush_cached_points_worker(influxdb_client, interval) -> None:
    """
    Background job that puts the points into the cache to be flushed according to the interval defined.

    :param influxdb_client:
    :param interval:
    :return: None
    """
    global stop_flag
    log.info('Flush worker started.')
    while not stop_flag:
        __flush_points(influxdb_client)
        gevent.sleep(interval / 1000)


def expose_metrics(influx_host: str = influx_host_ip,  # 'influxdb'/'10.0.10.16'
                   influx_port: int = 8086,
                   user: str = 'admin',
                   pwd: str = 'admin',
                   database: str = 'db_locust',
                   interval_ms: int = 1000) -> None:
    """
    Attach event handlers to locust EventHooks in order to persist information to influxdb.

    :param influx_host: InfluxDB hostname or IP.
    :param influx_port: InfluxDB port.
    :param user: InfluxDB username.
    :param pwd: InfluxDB password.
    :param database: InfluxDB database name. Will be created if not exist.
    :param interval_ms: Interval to save the data points to influxdb.
    """
    influxdb_client = InfluxDBClient(influx_host, influx_port, user, pwd, database)
    influxdb_client.create_database(database)
    node_id = 'local'
    if '--master' in sys.argv:
        node_id = 'master'
    if '--worker' in sys.argv:
        # TODO: Get real ID of slaves form locust somehow
        node_id = 'worker'
    # Start a greenlet that will save the data to influx according to the interval informed
    gevent.spawn(__flush_cached_points_worker, influxdb_client, interval_ms)
    # Request events
    events.request.add_listener(__listen_for_requests_events(node_id))
