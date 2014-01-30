from pylastica.aggregation.avg import Avg
from tests.base import Base
from pylastica.aggregation.globalagg import Global

__author__ = 'Joe Linn'

import unittest


class GlobalTest(unittest.TestCase, Base):
    def test_to_dict(self):
        expected = {
            "global": {},
            "aggs": {
                "avg_price": {"avg": {"field": "price"}}
            }
        }

        agg = Global("all_products").add_aggregation(Avg("avg_price").set_field("price"))
        self.assertEqual(expected, agg.to_dict())


if __name__ == '__main__':
    unittest.main()
