import csv

# Read CSV data and generate FDF content
def generate_fdf_content(csv_filename):
    fdf_content = '''%FDF-1.2
%âãÏÓ
1 0 obj
<< /FDF << /Fields 2 0 R >>
>>
endobj
2 0 obj
[ '''

    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            for key, value in row.items():
                fdf_content += f"<< /T ({key}) /V ({value}) >>\n"
                
        fdf_content += ']\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n'

    return fdf_content

# Write FDF content to a file
def write_fdf_file(fdf_content):
    with open('output.fdf', 'w') as fdf_file:
        fdf_file.write(fdf_content)

# Generate FDF content and write to a file
csv_filename = 'data.csv'
fdf_content = generate_fdf_content(csv_filename)
write_fdf_file(fdf_content)
