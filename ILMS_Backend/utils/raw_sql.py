from django.db import connection
from collections import namedtuple

from rest_framework.response import Response


class RawSQL(object):

    def __init__(self, sql, params):
        with connection.cursor() as self.cursor:
            self.cursor.execute(sql, params)

    def dict_fetchall(self):
        """Return all rows from a cursor as a dict"""
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def tuple_fetchall(self):
        """Return all rows from a cursor as a namedtuple"""
        nt_result = namedtuple('Result', [col[0] for col in self.cursor.description])
        return [nt_result(*row) for row in self.cursor.fetchall()]
