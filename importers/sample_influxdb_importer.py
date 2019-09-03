from influxdb_importer_base_class import InfluxdbImporter

class SampleInfluxdbImporter(InfluxdbImporter):

    def __init__(self, name, tags_dict):
        """
        - Each importer will have a unique name(name of its database in influxdb), and tags
        - There can be multiple importers with same name and different tags. In this case the data will go to the same
        database in inlfuxdb, but with different tags
        :param name:
        :param tags_dict:
        """
        super(SampleInfluxdbImporter, self).__init__(database_name=name)  # database name is same as name of importer
        self.tags_dict = tags_dict  # keep public so can update if need be

    def import_data(self, measurement, fields_list):
        """

        :param measurement:
        :param fields_list:
        :return:
        """
        self.enqueue_import(measurement=measurement, tags_dict=self.tags_dict, fields_list=fields_list)