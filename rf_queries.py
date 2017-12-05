LIST_ITEMS='''

/*
SELECT sono AS order_id, data_point, value, '2017-11-28 14:00:00.000000' as dts
  FROM connixt.report_data 
  WHERE sono LIKE 'RM%' 
 UNION
*/
SELECT cxid AS order_id, data_point, value, brec_ts as dts
  FROM connixt.adhoc_data 
  WHERE order_type = 'AMI Change Out' 
ORDER  BY dts

LIMIT 10

'''.strip()
