from collections import OrderedDict
CONFERENCES = OrderedDict()             # Avoid python < 3.7 incompatibility

# key should be higher case
# OK to have repeat conference name to build your favorites folder.
# don't forget add the conference infomation into the NAME_MAP below
CONFERENCES["SC"] = ["NDSS", "IEEE S&P", "USENIX", "CCS"]
CONFERENCES["SE"] = ["FSE", "ICSE", "ISSTA", "ASE"]

_tmp_conferences_list = [CONFERENCES[field] for field in CONFERENCES]
ALL_CONFERENCES_LIST = list(set([conf_name for field_list in _tmp_conferences_list for conf_name in field_list]))

# keep the KEY same to the name in CONFERENCES above
# Format of NAME_MAP
# KEY: CONF   or   KEY: (ASSOC, CONF)
# For example, if you open FSE 2000 in DBLP, the url is https://dblp.org/db/conf/sigsoft/fse2000.html
# sigsoft is ASSOC, fse is CONF, so we have: "FSE": ("sigsoft", "fse") (i.e, KEY: (ASSOC, CONF))
# sometimes ASSOC is same as CONF, like NDSS: https://dblp.org/db/conf/ndss/ndss2023.html
# so you can also use: "NDSS": "ndss" (i.e, KEY: CONF)
NAME_MAP = {
        "NDSS": "ndss", "IEEE S&P": "sp", "USENIX": "uss", "CCS": "ccs",
        "FSE": ("sigsoft", "fse"), "ICSE": "icse", "ISSTA": "issta", "ASE": ("kbse", "ase"),
        }