# %%
import pandas as pd

accident_dtypes = {
    # State / location identifiers
    'STATE':        'int8',
    'STATENAME':    'category',
    'ST_CASE':      'int32',      # primary join key — keep as int32
    'COUNTY':       'int16',
    'COUNTYNAME':   'category',
    'CITY':         'int16',
    'CITYNAME':     'category',

    # Person / vehicle counts
    'PEDS':         'int8',
    'PERNOTMVIT':   'int8',
    'VE_TOTAL':     'int8',
    'VE_FORMS':     'int8',
    'PVH_INVL':     'int8',
    'PERSONS':      'int8',
    'PERMVIT':      'int8',

    # Date / time
    'MONTH':        'int8',
    'MONTHNAME':    'category',
    'DAY':          'int8',
    'DAYNAME':      'category',
    'DAY_WEEK':     'int8',
    'DAY_WEEKNAME': 'category',
    'YEAR':         'int16',
    'HOUR':         'int8',
    'HOURNAME':     'category',
    'MINUTE':       'int8',
    'MINUTENAME':   'category',

    # Road identifiers (free text, keep as string)
    'TWAY_ID':      'object',
    'TWAY_ID2':     'object',

    # Road characteristics
    'ROUTE':        'int8',
    'ROUTENAME':    'category',
    'RUR_URB':      'int8',
    'RUR_URBNAME':  'category',
    'FUNC_SYS':     'int8',
    'FUNC_SYSNAME': 'category',
    'RD_OWNER':     'int8',
    'RD_OWNERNAME': 'category',
    'NHS':          'int8',
    'NHSNAME':      'category',
    'SP_JUR':       'int8',
    'SP_JURNAME':   'category',

    # Mile point (can be decimal)
    'MILEPT':       'float32',
    'MILEPTNAME':   'object',

    # Coordinates
    'LATITUDE':     'float32',
    'LATITUDENAME': 'object',
    'LONGITUD':     'float32',
    'LONGITUDNAME': 'object',

    # Crash characteristics
    'HARM_EV':      'int8',
    'HARM_EVNAME':  'category',
    'MAN_COLL':     'int8',
    'MAN_COLLNAME': 'category',
    'RELJCT1':      'int8',
    'RELJCT1NAME':  'category',
    'RELJCT2':      'int8',
    'RELJCT2NAME':  'category',
    'TYP_INT':      'int8',
    'TYP_INTNAME':  'category',
    'REL_ROAD':     'int8',
    'REL_ROADNAME': 'category',
    'WRK_ZONE':     'int8',
    'WRK_ZONENAME': 'category',

    # Conditions
    'LGT_COND':     'int8',
    'LGT_CONDNAME': 'category',
    'WEATHER':      'int8',
    'WEATHERNAME':  'category',

    # School bus / rail
    'SCH_BUS':      'int8',
    'SCH_BUSNAME':  'category',
    'RAIL':         'object',
    'RAILNAME':     'category',

    # Notification / arrival / hospital times
    'NOT_HOUR':     'int8',
    'NOT_HOURNAME': 'category',
    'NOT_MIN':      'int8',
    'NOT_MINNAME':  'category',
    'ARR_HOUR':     'int8',
    'ARR_HOURNAME': 'category',
    'ARR_MIN':      'int8',
    'ARR_MINNAME':  'category',
    'HOSP_HR':      'int8',
    'HOSP_HRNAME':  'category',
    'HOSP_MN':      'int8',
    'HOSP_MNNAME':  'category',

    # Target-adjacent — number of fatalities per crash
    'FATALS':       'int8',
}

accident = pd.read_csv("/Users/rohandasanoor/Downloads/FARS2024NationalCSV/accident.csv", dtype=accident_dtypes)
# %%
print(accident.head())