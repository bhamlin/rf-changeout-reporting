#!/usr/bin/python3

import localconfig
import pymssql
import rf_queries as rfq

from brec.db import MSSQL, PostgreSQL

c = PostgreSQL(localconfig.PGSQL_DSN)

new_meters = set()
for item in c.execute(rfq.CC_PSQL_NEW_METERS):
    meter = item['new_meter_number'].strip()
    # print(meter)
    if meter.isdigit():
        new_meters.add(meter)

# print(
#     rfq.CC_MSS_FIND_NEW_METERS.format("','".join(new_meters))
# )

m = MSSQL(*localconfig.MSS_DSN)

valid_meters = set()
for item in m.execute(rfq.CC_MSS_FIND_NEW_METERS.format("','".join(new_meters))):
    valid_meters.add(item[0].strip())

m.close()

print(valid_meters)
if valid_meters:
    c.execute_crud(rfq.CC_PSQL_SET_NEW_METERS.format("','".join(valid_meters)))
