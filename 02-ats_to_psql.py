#!/usr/bin/python3

import localconfig
import rf_queries as rfq

from brec.db import Oracle, PostgreSQL

c = PostgreSQL(localconfig.PGSQL_DSN)

old_meters = dict()
new_meters = dict()
for item in c.execute(rfq.ATS_PSQL_LIST_METERS_TO_ACCOUNT):
    meter = item['old_meter_number'].strip()
    if meter.isdigit():
        id = item['id']
        old_meters[meter] = {'id': id}
for item in c.execute(rfq.ATS_PSQL_LIST_NEW_METERS_TO_ACCOUNT):
    meter = item['new_meter_number'].strip()
    if meter.isdigit():
        id = item['id']
        new_meters[meter] = {'id': id}

########################
## ORACLE ZOOOOOOOONE ##
o = Oracle(localconfig.ORA_DSN)

for row in o.execute(rfq.ATS_ORAC_GET_ACCOUNTS_FOR_METER.format(
    "','".join(old_meters.keys()) )):
    meter, account, mapno = map(str, row)
    if meter in old_meters:
        old_meters[meter]['account'] = account
        old_meters[meter]['mapno'] = mapno
for row in o.execute(rfq.ATS_ORAC_GET_ACCOUNTS_FOR_METER.format(
    "','".join(new_meters.keys()) )):
    meter, account, mapno = map(str, row)
    if meter in new_meters:
        new_meters[meter]['account'] = account
        new_meters[meter]['mapno'] = mapno

o.close()
########################

for meter, data in old_meters.items():
    if (('id' in data and 'account' in data and 'mapno' in data)
     and (data['id'] and (data['account'] or data['mapno']))):
        print("+ {}, {}, {}".format(data['id'], data['account'], data['mapno']))
        c.execute_crud_args(rfq.ATS_PSQL_INSERT_ACCOUNT,
                data['id'], data['account'], data['mapno'])
        c.execute_crud_args(rfq.ATS_PSQL_SET_OLD_METER,
                data['id'])
    else:
        print("  {}".format(data))
for meter, data in new_meters.items():
    if (('id' in data and 'account' in data and 'mapno' in data)
     and (data['id'] and (data['account'] or data['mapno']))):
        print("+ {}, {}, {}".format(data['id'], data['account'], data['mapno']))
        c.execute_crud_args(rfq.ATS_PSQL_INSERT_ACCOUNT,
                data['id'], data['account'], data['mapno'])
        c.execute_crud_args(rfq.ATS_PSQL_SET_NEW_METER,
                data['id'])
    else:
        print("  {}".format(data))

c.close()
