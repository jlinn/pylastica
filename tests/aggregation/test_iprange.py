from pylastica import Document
from pylastica.aggregation.iprange import IpRange
from pylastica.doc_type import Mapping
from pylastica.query.query import Query
from tests.base import Base

__author__ = 'Joe Linn'

import unittest


class IpRangeTest(unittest.TestCase, Base):
    def setUp(self):
        super(IpRangeTest, self).setUp()
        self._index = self._create_index("test_aggregation_ip_range")
        mapping = Mapping()
        mapping.set_properties({
            "address": {"type": "ip"}
        })
        doc_type = self._index.get_doc_type("test")
        doc_type.mapping = mapping
        docs = [
            Document("1", {"address": "192.168.1.100"}),
            Document("2", {"address": "192.168.1.150"}),
            Document("3", {"address": "192.168.1.200"})
        ]
        doc_type.add_documents(docs)
        self._index.refresh()

    def tearDown(self):
        super(IpRangeTest, self).tearDown()
        self._index.delete()

    def test_ip_range_aggregation(self):
        agg = IpRange("ip", "address")
        agg.add_range(from_value="192.168.1.101").add_range(to_value="192.168.1.200").add_mask_range("192.168.1.0/24")

        query = Query()
        query.add_aggregation(agg)
        results = self._index.search(query).aggregations['ip']

        for bucket in results['buckets']:
            if 'from' in bucket and 'to' in bucket:
                #the CIDR mask
                self.assertEqual(3, bucket['doc_count'])
            else:
                self.assertEqual(2, bucket['doc_count'])


if __name__ == '__main__':
    unittest.main()
