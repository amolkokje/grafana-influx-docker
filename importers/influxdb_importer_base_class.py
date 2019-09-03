import logging
import time
import threading
import Queue
from datetime import datetime
from influxdb import InfluxDBClient

# REF: https://www.influxdata.com/blog/getting-started-python-influxdb/

class InfluxdbImporter(object):

    # TODO - make this all constants or pull from .env
    def __init__(self, database_name, host='localhost', port=8086, username='admin', password='admin'):
        """

        :param database_name:
        :param host:
        :param port:
        :param username:
        :param password:
        """
        self._database_name = database_name
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._log = logging.getLogger(self.__class__.__name__)
        self._influxdb_client = InfluxDBClient(host=host, port=port, username=username, password=password)

        # Create unique database for each importer
        self._create_database(database_name)

        # Initialize Queue, and start import thread
        self._import_queue = Queue.Queue()
        self._is_importing = False
        self.start_import()

    def _create_database(self, name):
        """

        :param name:
        :return:
        """
        database_list = [ db['name'] for db in self._influxdb_client.get_list_database() ]
        if name in database_list:
            self._log.info('Database with name {} already exists. Do not create a new database'.format(name))
        else:
            self._log.info('Creating database {}'.format(name))
            self._influxdb_client.create_database(name)

    def enqueue_import(self, measurement, tags_dict, fields_list):
        """
        Puts in Queue
        :param measurement: measurement name
        :param tags_dict: dict containing tags for the field data. for a measurement
        :param fields_list: list of dicts containing data with the same tag info, for given measurement
        :return:
        """
        data_list = []
        for field in fields_list:
            data_list.append({
                'measurement': measurement,
                'tags': tags_dict,
                'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'fields': field
            })
        self._import_queue.put(data_list)

    def start_import(self):
        """
        Starts thread to pull from Queue and import
        :return:
        """
        self._is_importing = True

        def import_thread():
            while self._is_importing:
                # empty the import queue if it contains data
                if not self._import_queue.empty():
                    self._influxdb_client.write_points(self._import_queue.get())
                else:
                    self.log.info('Import queue is empty!')
                    time.sleep(1)
            self.log.info('Importing stopped!')

        self._import_thread = threading.Thread(target=import_thread)
        self._import_thread.start()

    def stop_import(self):
        """
        Stop import thread
        :return:
        """
        self._is_importing = False