from django.test import (
    TestCase,
)

from ..utility.utils import get_readable_size


class TestGetReadableSize(TestCase):

    def test_size(self):
        """
        Testing the get_readable_size method using different combinations
        """

        size = 20
        expected = '20.0 B'
        self.assertEquals(get_readable_size(size), expected)

        size = 1024
        expected = '1.0 KB'
        self.assertEquals(get_readable_size(size), expected)

        size = 2048
        expected = '2.0 KB'
        self.assertEquals(get_readable_size(size), expected)

        size = 10000
        expected = '9.77 KB'
        self.assertEquals(get_readable_size(size), expected)

        size = 10000000
        expected = '9.54 MB'
        self.assertEquals(get_readable_size(size), expected)

        size = 20
        unit = 'KB'
        expected = '20.0 KB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 1024
        unit = 'KB'
        expected = '1.0 MB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 2048
        unit = 'KB'
        expected = '2.0 MB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000
        unit = 'KB'
        expected = '9.77 MB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000000
        unit = 'KB'
        expected = '9.54 GB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 20
        unit = 'MB'
        expected = '20.0 MB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 1024
        unit = 'MB'
        expected = '1.0 GB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 2048
        unit = 'KB'
        expected = '2.0 MB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000
        unit = 'MB'
        expected = '9.77 GB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000000
        unit = 'MB'
        expected = '9.54 TB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 20
        unit = 'GB'
        expected = '20.0 GB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 1024
        unit = 'GB'
        expected = '1.0 TB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 2048
        unit = 'GB'
        expected = '2.0 TB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000
        unit = 'GB'
        expected = '9.77 TB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000000
        unit = 'GB'
        expected = '9.54 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 20
        unit = 'TB'
        expected = '20.0 TB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 1024
        unit = 'TB'
        expected = '1.0 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 2048
        unit = 'TB'
        expected = '2.0 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000
        unit = 'TB'
        expected = '9.77 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 10000000
        unit = 'TB'
        expected = '9765.62 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 0
        unit = 'TB'
        expected = '0.0 B'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = -10
        unit = 'TB'
        expected = '0.0 B'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 20
        unit = 'PB'
        expected = '20.0 PB'
        self.assertEquals(get_readable_size(size, unit), expected)

        size = 20
        unit = 'PBS'
        expected = '0.0 B'
        self.assertEquals(get_readable_size(size, unit), expected)
