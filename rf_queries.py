LIST_ITEMS='''

SELECT sono AS order_id, data_point, value, '2017-11-28 14:00:00.000000' as dts
  FROM connixt.report_data 
  WHERE sono LIKE 'RM%' 
 UNION
SELECT cxid AS order_id, data_point, value, brec_ts as dts
  FROM connixt.adhoc_data 
  WHERE order_type = 'AMI Change Out' 
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
