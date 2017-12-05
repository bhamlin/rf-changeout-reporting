#!/usr/bin/python3

import localconfig
import rf_queries

from brec.db import PostgreSQL
from brec.connixt import rf_changeout as rfc

c = PostgreSQL(localconfig.PGSQL_DSN)

data=dict()
for item in c.execute(rf_queries.LIST_ITEMS):
    rfc.collect_rows(item, data)

for item, data in data.items():
    print(rfc.RF_Changeout.from_row(data).__dict__)



c.close()
