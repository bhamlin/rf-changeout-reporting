#!/usr/bin/python3

import localconfig

from brec.db import PostgreSQL

c = PostgreSQL(localconfig.PGSQL_DSN)
