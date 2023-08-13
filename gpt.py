import csv
from pdfrw import PdfReader, PdfWriter

def read_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

#def populate_pdf_form(pdf_template_path, csv_data):
#    pdf = PdfReader(pdf_template_path)
#    annotations = pdf.pages[0]['/Annots']
#
#    for row in csv_data:
#        field_name = row[0]  # Assuming the first column of CSV has field names
#        field_value = row[1]  # Assuming the second column of CSV has field values
#
#        for annotation in annotations:
#            if annotation['/T'] == field_name:
#                annotation.update({
#                    PdfName('/V'): field_value,
#                    PdfName('/AS'): PdfName('/Off')
#                })
#
#    output_pdf_path = 'output_populated.pdf'
#    PdfWriter().write(output_pdf_path, pdf)

def main():
    csv_file_path = 'list.csv'
    #pdf_template_path = 'form.pdf'

    csv_data = read_csv(csv_file_path)
    for row in csv_data[:10]:
        print(row)
    #populate_pdf_form(pdf_template_path, csv_data)

if __name__ == '__main__':
    main()
