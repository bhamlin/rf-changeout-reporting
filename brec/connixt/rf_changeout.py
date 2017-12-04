
# (raw name, table column)
COLS=[
    ('cxid', 'cxid'),
    ('dts', 'dts'),
    ('Existing Meter Number', 'old_meter_number'),
    ('Existing Meter Reading', 'old_meter_reading'),
    ('New Meter Number', 'new_meter_number'),
    ('New Meter Reading', 'new_meter_reading'),
    ('Geo Tag', 'geo_tag'),
    ('GPS', 'gps'),
    ('SRV Man Initials', 'initials'),
    ('Meter Site Insp.', 'insp_state'),
    ('Meter Site Insp. Notes', 'insp_notes'),
    # ('SO No', 'sono'),
    # ('Map No', 'mapno'),
    ('Photo1', 'photo1'),
    ('Photo2', 'photo2'),
    ('Photo3', 'photo3')
]

def collect_rows(row, data):
    oid = row['order_id']
    key = row['data_point']
    val = row['value']
    if not oid in data:
        data[oid] = dict()
    data[oid][key] = val

def row_to_record(row):
    output = list()
    for field, col in COLS:
        if field in row:
            output.append(row[field])
        else:
            output.append(None)
    return output
