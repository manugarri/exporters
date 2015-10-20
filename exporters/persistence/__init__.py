from exporters.persistence.exporter_api_persistence import ExporterApiPersistence
from .pickle_persistence import PicklePersistence
from .alchemy_persistence import MysqlPersistence, PostgresqlPersistence

PERSISTENCE_LIST = [PicklePersistence, MysqlPersistence, PostgresqlPersistence, ExporterApiPersistence]