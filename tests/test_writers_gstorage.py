import mock
import unittest
from contextlib import nested

from exporters.records.base_record import BaseRecord
from exporters.writers.gstorage_writer import GStorageWriter
from exporters.writers.base_writer import InconsistentWriteState

from .utils import meta


class GStorageWriterTest(unittest.TestCase):
    def get_items_to_write(self):
        data = [
            {'name': 'Roberto', 'birthday': '12/05/1987'},
            {'name': 'Claudia', 'birthday': '21/12/1985'},
        ]
        return [BaseRecord(d) for d in data]

    def get_options(self):
        return {
            'name': 'exporters.writers.gstorage_writer.GStorageWriter',
            'options': {
                'project': 'some-project-666',
                'bucket': 'bucket-777',
                'credentials': {
                    "type": "service_account",
                    "private_key_id": "xxx",
                    "private_key": "yyy",
                },
                'filebase': 'tests/',
            }
        }

    def test_write(self):
        items_to_write = self.get_items_to_write()
        options = self.get_options()

        with mock.patch('gcloud.storage.Client.from_service_account_json') as mocked:
            writer = GStorageWriter(options, meta())
            writer.write_batch(items_to_write)
            writer.flush()
            writer.close()
            mocked.assert_has_calls([('().bucket().blob().upload_from_file',
                                      (mock.ANY,))])

    @mock.patch('gcloud.storage.Client.from_service_account_json')
    def test_write_blob_consistency(self, get_client):
        get_client().bucket().blob().size = 999
        get_client().bucket().blob().md5_hash = "a"*24
        # given
        items_to_write = self.get_items_to_write()
        options = self.get_options()
        options['options']['check_consistency'] = True

        # when:
        writer = GStorageWriter(options, meta())
        try:
            writer.write_batch(items_to_write)
            writer.flush()
        finally:
            writer.close()

        with self.assertRaises(InconsistentWriteState):
            writer.finish_writing()

    def test_init_from_resource(self):
        options = {
            'name': 'exporters.writers.gstorage_writer.GStorageWriter',
            'options': {
                'project': 'some-project-666',
                'bucket': 'bucket-777',
                'filebase': 'tests/',
            }
        }
        env = {'EXPORTERS_GSTORAGE_CREDS_RESOURCE': 'a:b'}
        with nested(mock.patch.dict('os.environ', env),
                    mock.patch('pkg_resources.resource_string', return_value='{}'),
                    mock.patch('gcloud.storage.Client.from_service_account_json')):
            GStorageWriter(options, meta())

    def test_init_fails_with_bad_resource(self):
        options = {
            'name': 'exporters.writers.gstorage_writer.GStorageWriter',
            'options': {
                'project': 'some-project-666',
                'bucket': 'bucket-777',
                'filebase': 'tests/',
            }
        }
        env = {'EXPORTERS_GSTORAGE_CREDS_RESOURCE': 'a:b'}
        with nested(self.assertRaisesRegexp(ImportError, 'No module named a'),
                    mock.patch.dict('os.environ', env)):
            GStorageWriter(options, meta())
