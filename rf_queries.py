GET_LAST_ENTRY='''

select max(dts) from hunt.rf_changeout_data

'''.strip()

LIST_ITEMS='''

SELECT sono AS order_id, data_point, value, brec_ts as dts
  FROM connixt.report_data 
  WHERE sono LIKE 'RM%' and brec_ts > '{0}'
 UNION
SELECT cxid AS order_id, data_point, value, brec_ts as dts
  FROM connixt.adhoc_data 
  WHERE order_type = 'AMI Change Out' and brec_ts > '{0}'
ORDER  BY dts

'''.strip()

GET_RFC_ENTRY='''

SELECT id
FROM hunt.rf_changeout_data
WHERE cxid = %s

'''.strip()

RFC_INSERT_CXID='''

INSERT INTO hunt.rf_changeout_data (
    cxid, old_meter_number, old_meter_reading, new_meter_number, new_meter_reading, dts
)
VALUES (%s, %s, %s, %s, %s, %s)

'''.strip()

RFC_INSERT_LOC='''

INSERT INTO hunt.rf_changeout_loc (
    data_id, gps_x, gps_y, geo_tag
)
VALUES (%s, %s, %s, %s)

'''.strip()

RFC_INSERT_PHOTOS='''

INSERT INTO hunt.rf_changeout_photos (
    data_id, photo_url_1, photo_url_2, photo_url_3
)
VALUES (%s, %s, %s, %s)

'''.strip()

RFC_INSERT_SITE_INSP='''

INSERT INTO hunt.rf_changeout_site_insp (
    data_id, initials, insp_state, insp_notes
)
VALUES (%s, %s, %s, %s)

'''.strip()

RFC_INSERT_ATS='''

INSERT INTO hunt.rf_changeout_ats (
    data_id
)
VALUES (%s)

'''.strip()

RFC_INSERT_CC='''

INSERT INTO hunt.rf_changeout_cc (
    data_id
)
VALUES (%s)

'''.strip()

ATS_PSQL_LIST_METERS_TO_ACCOUNT='''

select cd.id, cd.old_meter_number
from hunt.rf_changeout_data cd
  left join hunt.rf_changeout_ats_data ad on cd.id = ad.data_id
where ad.account_number is null or ad.map_number is null

'''.strip()

ATS_PSQL_LIST_NEW_METERS_TO_ACCOUNT='''

select cd.id, cd.new_meter_number
from hunt.rf_changeout_data cd
  left join hunt.rf_changeout_ats ad on cd.id = ad.data_id
where ad.new_meter_on_account = 'f'

'''.strip()

# ATS_ORAC_GET_ACCOUNTS_FOR_METER='''
# 
# select sm.meterno, am.accountno, loc.name as mapno
# from CISDATA.SERVICE_METERS sm
#   left join CISDATA.ACCOUNT_MASTER am on sm.LOCATION_ID = am.LOCATION_ID
#   left join CISDATA.ACCOUNT_STATUS ams on am.ACCOUNT_STATUS_ID = ams.ACCOUNT_STATUS_ID
#   left join FMDATA.LOCATION loc on sm.LOCATION_ID = loc.LOCATION_ID
# where (ams.ACCOUNT_STATUS_DESC != 'Inactive') and (sm.meterno in ('{}'))
# 
# '''.strip()

ATS_ORAC_GET_ACCOUNTS_FOR_METER='''

SELECT sm.meterno, am.accountno, loc.name AS mapno
FROM cisdata.service_meters sm
    LEFT JOIN cisdata.account_master am ON sm.location_id = am.location_id
    LEFT JOIN cisdata.account_status ams ON am.account_status_id = ams.account_status_id
    LEFT JOIN fmdata.location loc ON sm.location_id = loc.location_id
WHERE
    ( ams.account_status_desc != 'Inactive' )
    AND   ( sm.meterno IN ('{0}') )
UNION
SELECT meterno, accountno, mapno
FROM (  SELECT sm.meterno, am.accountno, loc.name AS mapno,
            RANK() OVER(
                PARTITION BY loc.name
                ORDER BY
                    am.disconnect_date DESC
            ) AS loc_rnk
        FROM cisdata.service_meters sm
            LEFT JOIN cisdata.account_master am ON sm.location_id = am.location_id
            LEFT JOIN cisdata.account_status ams ON am.account_status_id = ams.account_status_id
            LEFT JOIN fmdata.location loc ON sm.location_id = loc.location_id
        WHERE
            ( ams.account_status_desc = 'Inactive' )
            AND   ( sm.meterno IN ( '{0}' ) )
    ) data
WHERE loc_rnk = 1
'''.strip()

ATS_PSQL_INSERT_ACCOUNT='''

INSERT INTO hunt.rf_changeout_ats_data(
            data_id, account_number, map_number)
    VALUES (%s, %s, %s);

'''.strip()

ATS_PSQL_SET_OLD_METER='''

UPDATE hunt.rf_changeout_ats
   SET old_meter_on_account='t'
 WHERE data_id=%s;

'''.strip()

ATS_PSQL_SET_NEW_METER='''

UPDATE hunt.rf_changeout_ats
   SET old_meter_on_account='t', new_meter_on_account='t'
 WHERE data_id=%s;

'''.strip()

CC_PSQL_NEW_METERS='''

select cd.new_meter_number
   FROM hunt.rf_changeout_data cd
     left join hunt.rf_changeout_ats ad on cd.id = ad.data_id
     left join hunt.rf_changeout_cc cc on cd.id = cc.data_id
   where ad.new_meter_on_account = False
     and ad.old_meter_on_account = True
     and cc.new_meter_exists = False

'''.strip()

CC_PSQL_SET_NEW_METERS='''

update hunt.rf_changeout_cc
  set new_meter_exists = True
where data_id in (select id
    from hunt.rf_changeout_data cd
    where cd.new_meter_number in (
      '{}'
    ))

'''.strip()

CC_MSS_FIND_NEW_METERS='''

select meterNo
from Meters m
where meterNo in ('{}')

'''.strip()
