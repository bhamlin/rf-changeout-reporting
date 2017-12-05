
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
DATA_FIELDS=[
    'cxid',
    'old_meter_number',
    'old_meter_reading',
    'new_meter_number',
    'new_meter_reading',
    'dts'
]
LOC_FIELDS=[
    'id',
    'gps_x',
    'gps_y',
    'geo_tag'
]
PHOTO_FIELDS=[
    'id',
    'photo1',
    'photo2',
    'photo3'
]
SITE_INSP_FIELDS=[
    'id',
    'initials',
    'insp_state',
    'insp_notes'
]

class RF_Changeout():
    @staticmethod
    def from_row(row):
        self = RF_Changeout()
        for key, col in COLS:
            if key in row:
                setattr(self, col, row[key])
        self.fix_gps()
        return self

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def fix_gps(self):
        gps = getattr(self, 'gps', None)
        if gps:
            u, v = gps.replace(' ', '').split(',')
            if u and v:
                self.gps_x = float(u) # Latitude
                self.gps_y = float(v) # Longitude
                del self.gps

    def get_data(self):
        result=list()
        for field in DATA_FIELDS:
            result.append(self[field])
        return result

    def get_loc(self):
        result=list()
        for field in LOC_FIELDS:
            result.append(self[field])
        return result
    
    def get_photos(self):
        result=list()
        for field in PHOTO_FIELDS:
            result.append(self[field])
        return result

    def get_site_insp(self):
        result=list()
        for field in SITE_INSP_FIELDS:
            result.append(self[field])
        return result

def collect_rows(row, data):
    oid = row['order_id']
    key = row['data_point']
    val = row['value']
    if not oid in data:
        data[oid] = dict()
        data[oid]['dts'] = row['dts']
    data[oid][key] = val
