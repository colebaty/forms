#!/usr/bin/env python

import csv
from datetime import datetime
import tempfile

# "constants" for PDF form
dodaac_from=b'NO0060'
dodaac_to=b'SX1493'
cond_code=b'D'
units=b'EA'
docid=b'A5J'
POC_INFO=b'POC:  KARL HUNDER  Email:  khunder@fti-net.com  TEL. NO:  (xxx) xxx-xxxx'
mark_for=b'>'

# FDF file info stuff
fdf_header = '''%FDF-1.2
%âãÏÓ
1 0 obj
<< /FDF << /Fields 2 0 R >>
>>
endobj
2 0 obj
[ '''

fdf_footer = '''
endobj
trailer
<< /Root 1 0 R >>
%%EOF
'''

fdf_content = ''

id = 1 # for document numbers


# read in csv data

# while there are records
    # generate FDF
    # populate PDF

