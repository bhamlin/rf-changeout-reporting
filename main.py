#!/usr/bin/python3

import localconfig
import rf_queries as rfq

from brec.db import PostgreSQL
from brec.connixt import rf_changeout as rfc

def S(generator):
    result = None
    for result in generator:
        pass
    return result

c = PostgreSQL(localconfig.PGSQL_DSN)

data=dict()
for item in c.execute(rfq.LIST_ITEMS):
    rfc.collect_rows(item, data)

for item, data in data.items():
    meter = rfc.RF_Changeout.from_row(data)

    id = S(c.execute_args(rfq.GET_RFC_ENTRY, meter.cxid))
    if not id:
        c.execute_crud_args(rfq.RFC_INSERT_CXID, *meter.get_data())
        id = S(c.execute_args(rfq.GET_RFC_ENTRY, meter.cxid))['id']
        meter['id'] = id
        c.execute_crud_args(rfq.RFC_INSERT_LOC, *meter.get_loc())
        c.execute_crud_args(rfq.RFC_INSERT_PHOTOS, *meter.get_photos())
        c.execute_crud_args(rfq.RFC_INSERT_SITE_INSP, *meter.get_site_insp())
        
        c.execute_crud_args(rfq.RFC_INSERT_ATS, id)
        c.execute_crud_args(rfq.RFC_INSERT_CC, id)

c.close()

print()
