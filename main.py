#!/usr/bin/python3

import localconfig
import rf_queries

from brec.db import PostgreSQL
from brec.connixt import rf_changeout

c = PostgreSQL(localconfig.PGSQL_DSN)

data=dict()
for item in c.execute(rf_queries.LIST_ITEMS):
    rf_changeout.collect_rows(item, data)

for item, data in data.items():
    print(rf_changeout.row_to_record(data))

c.close()
