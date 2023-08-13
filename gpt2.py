import csv
import PyPDF2

def read_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def populate_pdf_form(pdf_template_path, csv_data):
    pdf = PyPDF2.PdfReader(pdf_template_path)
    pdf_writer = PyPDF2.PdfWriter()

    for row in csv_data:
        field_name = row[0]
        field_value = row[1]

        for page in pdf.pages:
            annotations = page['/Annots']
            if annotations:
                for annotation in annotations:
                    annotation_obj = annotation.get_object()
                    if annotation_obj['/T'] == field_name:
                        annotation_obj.update({
                            PyPDF2.PdfName('/V'): PyPDF2.create_string_object(field_value),
                            PyPDF2.PdfName('/AS'): PyPDF2.PdfName('/Off')
                        })
        pdf_writer.add_page(page)

    output_pdf_path = 'output_populated.pdf'
    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def main():
    csv_file_path = 'data.csv'
    pdf_template_path = 'template.pdf'

    csv_data = read_csv(csv_file_path)
    populate_pdf_form(pdf_template_path, csv_data)

if __name__ == '__main__':
    main()
