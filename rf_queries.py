LIST_ITEMS='''

SELECT sono AS order_id, data_point, value 
  FROM connixt.report_data 
  WHERE sono LIKE 'RM%' 
 UNION 
SELECT cxid AS order_id, data_point, value 
  FROM connixt.adhoc_data 
  WHERE order_type = 'AMI Change Out' 
ORDER  BY order_id, data_point

'''.strip()
