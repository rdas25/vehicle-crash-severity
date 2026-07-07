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

person_dtypes = {
    # Identifiers
    'STATE':            'int8',
    'STATENAME':        'category',
    'ST_CASE':          'int32',
    'VEH_NO':           'int16',
    'PER_NO':           'int8',
    'VE_FORMS':         'int8',
    'COUNTY':           'int16',

    # Date / time
    'MONTH':            'int8',
    'MONTHNAME':        'category',
    'DAY':              'int8',
    'DAYNAME':          'category',
    'HOUR':             'int8',
    'HOURNAME':         'category',
    'MINUTE':           'int8',
    'MINUTENAME':       'category',

    # Crash characteristics
    'HARM_EV':          'int8',
    'HARM_EVNAME':      'category',
    'MAN_COLL':         'int8',
    'MAN_COLLNAME':     'category',
    'SCH_BUS':          'int8',
    'SCH_BUSNAME':      'category',
    'RUR_URB':          'int8',
    'RUR_URBNAME':      'category',
    'FUNC_SYS':         'int8',
    'FUNC_SYSNAME':     'category',

    # Vehicle info
    'MOD_YEAR':         'int16',
    'MOD_YEARNAME':     'category',
    'VPICMAKE':         'int16',
    'VPICMAKENAME':     'category',
    'VPICMODEL':        'int16',
    'VPICMODELNAME':    'category',
    'VPICBODYCLASS':    'int16',
    'VPICBODYCLASSNAME':'category',
    'MAKE':             'int16',
    'MAKENAME':         'category',
    'BODY_TYP':         'int16',
    'BODY_TYPNAME':     'category',
    'ICFINALBODY':      'int16',
    'ICFINALBODYNAME':  'category',
    'GVWR_FROM':        'int8',
    'GVWR_FROMNAME':    'category',
    'GVWR_TO':          'int8',
    'GVWR_TONAME':      'category',
    'TOW_VEH':          'int8',
    'TOW_VEHNAME':      'category',
    'SPEC_USE':         'int8',
    'SPEC_USENAME':     'category',
    'EMER_USE':         'int8',
    'EMER_USENAME':     'category',
    'ROLLOVER':         'int8',
    'ROLLOVERNAME':     'category',
    'IMPACT1':          'int8',
    'IMPACT1NAME':      'category',
    'FIRE_EXP':         'int8',
    'FIRE_EXPNAME':     'category',
    'MAK_MOD':          'int16',
    'MAK_MODNAME':      'category',

    # Person info
    'AGE':              'int16',
    'AGENAME':          'category',
    'SEX':              'int8',
    'SEXNAME':          'category',
    'PER_TYP':          'int8',
    'PER_TYPNAME':      'category',

    # Target variable
    'INJ_SEV':          'int8',
    'INJ_SEVNAME':      'category',

    # Safety equipment
    'SEAT_POS':         'int8',
    'SEAT_POSNAME':     'category',
    'REST_USE':         'int8',
    'REST_USENAME':     'category',
    'REST_MIS':         'int8',
    'REST_MISNAME':     'category',
    'HELM_USE':         'int8',
    'HELM_USENAME':     'category',
    'HELM_MIS':         'int8',
    'HELM_MISNAME':     'category',
    'AIR_BAG':          'int8',
    'AIR_BAGNAME':      'category',

    # Ejection
    'EJECTION':         'int8',
    'EJECTIONNAME':     'category',
    'EJ_PATH':          'int8',
    'EJ_PATHNAME':      'category',
    'EXTRICAT':         'int8',
    'EXTRICATNAME':     'category',

    # Alcohol / drugs
    'DRINKING':         'int8',
    'DRINKINGNAME':     'category',
    'ALC_STATUS':       'int8',
    'ALC_STATUSNAME':   'category',
    'ATST_TYP':         'int8',
    'ATST_TYPNAME':     'category',
    'ALC_RES':          'float32',
    'ALC_RESNAME':      'category',
    'DRUGS':            'int8',
    'DRUGSNAME':        'category',
    'DSTATUS':          'int8',
    'DSTATUSNAME':      'category',

    # Hospital / death info (post-crash, drop before modeling)
    'HOSPITAL':         'int8',
    'HOSPITALNAME':     'category',
    'DOA':              'int8',
    'DOANAME':          'category',
    'DEATH_MO':         'int8',
    'DEATH_MONAME':     'category',
    'DEATH_DA':         'int8',
    'DEATH_DANAME':     'category',
    'DEATH_YR':         'int16',
    'DEATH_YRNAME':     'category',
    'DEATH_TM':         'int16',
    'DEATH_TMNAME':     'category',
    'DEATH_HR':         'int8',
    'DEATH_HRNAME':     'category',
    'DEATH_MN':         'int8',
    'DEATH_MNNAME':     'category',
    'LAG_HRS':          'int16',
    'LAG_HRSNAME':      'category',
    'LAG_MINS':         'int8',
    'LAG_MINSNAME':     'category',

    # Miscellaneous
    'STR_VEH':          'int8',
    'DEVTYPE':          'int8',
    'DEVTYPENAME':      'category',
    'DEVMOTOR':         'int8',
    'DEVMOTORNAME':     'category',
    'LOCATION':         'int8',
    'LOCATIONNAME':     'category',
    'WORK_INJ':         'int8',
    'WORK_INJNAME':     'category',
    'HISPANIC':         'int8',
    'HISPANICNAME':     'category',
}

accident = pd.read_csv("/Users/rohandasanoor/Downloads/FARS2024NationalCSV/accident.csv")
person = pd.read_csv("/Users/rohandasanoor/Downloads/FARS2024NationalCSV/person.csv")
# %%
print(accident.head())
print(person.head())
# %%
