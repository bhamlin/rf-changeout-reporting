#!/usr/bin/python3

import localconfig
import rf_queries

from brec.db import PostgreSQL
from brec.connixt import rf_changeout

c = PostgreSQL(localconfig.PGSQL_DSN)

for item in c.execute(rf_queries.LIST_ITEMS):
    print(item)

c.close()
