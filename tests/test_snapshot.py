from time import sleep
from pylastica.document import Document
from pylastica.exception import NotFoundException
from pylastica.query.matchall import MatchAll
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class SnapshotTest(unittest.TestCase, Base):
    def setUp(self):
        super(SnapshotTest, self).setUp()
        self._snapshot = self._get_client().snapshot

        self._index = self._create_index("test_snapshot")
        self._docs = [
            Document("1", {"city": "San Diego"}),
            Document("2", {"city": "San Luis Obispo"}),
            Document("3", {"city": "San Francisco"})
        ]
        self._index.get_doc_type("test").add_documents(self._docs)
        self._index.refresh()

    def tearDown(self):
        super(SnapshotTest, self).tearDown()
        self._index.delete()

    def test_register_repository(self):
        name = "test_register"
        location = "/tmp/test_register"

        response = self._snapshot.register_repository(name, "fs", {"location": location})
        self.assertTrue(response.is_ok())

        response = self._snapshot.get_repository(name)
        self.assertEqual(location, response["settings"]["location"])

        # attempt to retrieve a repository which does not exist
        self.assertRaises(NotFoundException, self._snapshot.get_repository, "foobar")

    def test_snapshot_restore(self):
        repository_name = "test_repository"
        location = "/tmp/%s" % repository_name

        # register a repository
        response = self._snapshot.register_repository(repository_name, "fs", {"location": location})
        self.assertTrue(response.is_ok())

        # create a snapshot of our test index
        snapshot_name = "test_snapshot_1"
        response = self._snapshot.create_snapshot(repository_name, snapshot_name, {"indices": self._index.name}, True)

        # ensure that the snapshot was created properly
        self.assertTrue(response.is_ok())
        self.assertIn("snapshot", response.data)
        self.assertIn(self._index.name, response.data["snapshot"]["indices"])
        self.assertEqual(1, len(response.data["snapshot"]["indices"]))  # only the specified index should be present
        self.assertEqual(snapshot_name, response.data["snapshot"]["snapshot"])

        # retrieve data regarding the snapshot
        response = self._snapshot.get_snapshot(repository_name, snapshot_name)
        self.assertIn(self._index.name, response["indices"])

        # delete our test index
        self._index.delete()

        # restore the test index from our snapshot
        response = self._snapshot.restore_snapshot(repository_name, snapshot_name)
        self.assertTrue(response.is_ok())

        sleep(1) # give ES time to restore the index

        # ensure that the index has been restored
        count = self._index.get_doc_type("test").count(MatchAll())
        self.assertEqual(len(self._docs), count)

        # delete the snapshot
        response = self._snapshot.delete_snapshot(repository_name, snapshot_name)
        self.assertTrue(response.is_ok())

        # ensure that the snapshot has been deleted
        self.assertRaises(NotFoundException, self._snapshot.get_snapshot, repository_name, snapshot_name)

if __name__ == '__main__':
    unittest.main()
