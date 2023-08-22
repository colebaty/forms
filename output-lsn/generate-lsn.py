import csv
import re
import tempfile
from datetime import datetime
import os

# FDF stuff
fdf_header = '''%FDF-1.2
%âãÏÓ
1 0 obj
<< /FDF << /Fields 2 0 R >>
>>
endobj
2 0 obj
[ '''
fdf_footer = ']\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n'
fdf_content = ""


# "constants" for PDF form
fdf_static_content = {
    'DODAAC_FROM': 'N00060',
    'DODAAC_TO': 'SX1493',
    'COND_CODE': 'D',
    'UNITS': 'EA',
    'DOCID': 'A5J',
    'POC_INFO': 'POC:  KARL HUNDER  EMAIL:  KHUNDER@FTI-NET.COM  TEL. NO: (757) 230-2216',
    'PART_NO': '',
    #'MARK_FOR': '>'
}

# DOCNO stuff
id = 1
def getDocNo():
    day_of_year = str(datetime.today().timetuple().tm_yday)
    julian_year = str(datetime.today().timetuple().tm_year)[3:]
    
    global id
    docNo = fdf_static_content['DODAAC_FROM'] + julian_year + day_of_year + f'{id:0>{4}}'
    id += 1
    return docNo


csv_file = open('list.csv', 'r')
csv_reader = csv.DictReader(csv_file)

nsn_pattern = r'NSN_DATA'

barcode_dict = {
    'NSN_DATA': "<< /T (NSN_BARCODE) /V (**) >>\n",
    'DOCNO_BARCODE': "<< /T (DOCNO_BARCODE) /V (**) >>\n",
    'DOCNO_TEXT': "<< /T (DOCNO_TEXT) /V (**) >>\n"
}

addtl_data_line = "<< /T (ADDTL_DATA1) /V (**) >>\n"
addtl_data_template = f'PART NUMBER: | MODEL NUMBER: '
for row in csv_reader:
    fdf_content = ""
    for key, value in fdf_static_content.items():
        fdf_content += f"<< /T ({key}) /V ({value}) >>\n"

    # price stuff
    total_price = int(row['QTY']) * float(row['UNIT_PRICE'])
    #print(f'total_price: {total_price:.2f}')
    fdf_content += f"<< /T (TOTAL_PRICE) /V ({total_price:.2f}) >>\n"

    # DOCNO stuff
    docNo = getDocNo()
    #print(f'docNo: {docNo}')
    docNo_text = barcode_dict['DOCNO_TEXT']
    docNo_text = re.sub(r"\*\*", f'{docNo}', docNo_text)
    docNo_barcode = barcode_dict['DOCNO_BARCODE']
    docNo_barcode = re.sub(r"\*\*", f'*{docNo}*', docNo_barcode)
    fdf_content += docNo_text + docNo_barcode

    # part, model number stuff
    addtl_data = addtl_data_template
    for key, value in row.items():
        if re.search(r'PART #', key):
            matches = re.match(r"(.*)( \| )(.*)", addtl_data)
            addtl_data = f'{matches.group(1)}{value} {matches.group(2)}{matches.group(3)}'
            continue
        if re.search(r'Model #', key):
            matches = re.match(r"(.*)( \| )(.*)", addtl_data)
            addtl_data = f'{matches.group(1)}{matches.group(2)}{matches.group(3)}{value}'
            continue

        fdf_content += f"<< /T ({key}) /V ({value}) >>\n"

        if re.search(nsn_pattern, key):
            barcode = barcode_dict[key]
            barcode = re.sub(r"\*\*", f'*{value}*', barcode)
            fdf_content += barcode
    
    #print(f'addtl_data:{addtl_data}')
    addtl_data_content = re.sub(r"\*\*", addtl_data, addtl_data_line)
    #print(f'addtl_data_content: {addtl_data_content}')
    fdf_content += addtl_data_content
    print(f'{fdf_content}\n')
    with tempfile.NamedTemporaryFile(suffix='.fdf', dir='/tmp') as temp_file:
        with open(temp_file.file.name, 'w') as fdf_file:
            fdf_file.write(fdf_header + fdf_content + fdf_footer)
        os.system(f'pdftk ../barcode_test.pdf fill_form "{fdf_file.name}" output "./output-{docNo}-lsn.pdf" flatten')

os.system(f'pdftk ./output-*.pdf cat output ./turn-in-forms-with-lsn.pdf')
