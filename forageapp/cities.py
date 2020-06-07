CITY_MAP = {
    "la": ["06037"],
    "dc": ["11001", "51013"],
    "chicago": ["17031"],
    "nyc": [
        "36047",  # Brooklyn
        "36061",  # Manhattan
        "36005",  # Bronx
        "36085",  # Staten Island
        "36081",  # Queens
    ],
    'houstan': ['48201'],
    'phoenix': ['04013'],
    'philly': ['42101'],
    'san_antonio': ['48029'],
    'san_diego': ['06073'],
    'dallas_fw': ['48113', '48439'],
    'san_jose': ['06085'],
    'austin': ['48453'],
    'jacksonville': ['12031'],
    'columbus': ['39049'],
    'charlotte': ['37119'],
    'sf': ['06075'],
    'seattle': ['53033'],
    'denver': ['08031'],
    'boston': ['25025'],
    'detroit': ['26163'],
    'wilmington': ['10003']
}

COUNTY_TO_CITY_MAP = {}
for city, county_list in CITY_MAP.items():
    for county_fips in county_list:
        COUNTY_TO_CITY_MAP[county_fips] = city

SAVE_TO_DISPLAY_NAME = {
    'la': 'Los Angeles',
    'nyc': 'New York City',
    'chicago': 'Chicago',
    'dc': 'Washington D.C.',
    'houstan': 'Houston', # lol
    'phoenix': 'Phoenix',
    'philly': 'Philadelphia',
    'san_antonio': 'San Antonio',
    'san_diego': 'San Diego',
    'dallas_fw': 'Dallas-Fort-Worth',
    'san_jose': 'San Jose',
    'austin': 'Austin',
    'jacksonville': 'Jacksonville',
    'columbus': 'Columbus',
    'charlotte': 'Charlotte',
    'sf': 'San Francisco',
    'seattle': 'Seattle',
    'denver': 'Denver',
    'boston': 'Boston',
    'detroit': 'Detroit',
    'wilmington': 'Wilmington DE'
}

DISPLAY_TO_SAVE_NAME = {v: k for k, v in SAVE_TO_DISPLAY_NAME.items()}