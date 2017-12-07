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

ATS_ORAC_GET_ACCOUNTS_FOR_METER='''

select sm.meterno, am.accountno, loc.name as mapno
from CISDATA.SERVICE_METERS sm
  left join CISDATA.ACCOUNT_MASTER am on sm.LOCATION_ID = am.LOCATION_ID
  left join CISDATA.ACCOUNT_STATUS ams on am.ACCOUNT_STATUS_ID = ams.ACCOUNT_STATUS_ID
  left join FMDATA.LOCATION loc on sm.LOCATION_ID = loc.LOCATION_ID
where ams.ACCOUNT_STATUS_DESC != 'Inactive' and sm.meterno in ('{}')

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
