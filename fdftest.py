import csv
import tempfile

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

csv_file = open('test.csv', 'r')
csv_reader = csv.DictReader(csv_file)
for row in csv_reader:
    for key, value in row.items():
        fdf_content += f"<< /T ({key}) /V ({value}) >>\n"

    print(fdf_content)
    with tempfile.NamedTemporaryFile(suffix='.fdf', dir='/tmp', delete=False) as temp_file:
        with open(temp_file.file.name, 'w') as fdf_file:
            fdf_file.write(fdf_header + fdf_content + fdf_footer)


