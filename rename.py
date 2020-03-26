import io
import os
from  PyPDF2 import PdfFileWriter, PdfFileReader
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

input_PDF = PdfFileReader(open('163.pdf', 'rb'))

# функция извлечения текста из pdf
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    if text:
        return text

##########################################################################################
if __name__ == '__main__':
    # читаем постранично pdf
    for i in range(input_PDF.getNumPages()):
        output = PdfFileWriter()
        new_File_PDF = input_PDF.getPage(i)
        output.addPage(new_File_PDF)
        output_Name_File = "163-" + str(i + 1) + ".pdf" #временное название файла
        outputStream = open(output_Name_File, 'wb')
        output.write(outputStream)
        outputStream.close()
        #переименовываем файл по номеру лицевого счета
        pdf_Text = extract_text_from_pdf(output_Name_File)
        index = pdf_Text.find("0163")
        new_NamePdf = pdf_Text[index:index + 8]  + ".pdf" # нашли номер лицевого счета и вывели его 8 символов
        os.rename(output_Name_File, new_NamePdf)
        print (new_NamePdf)
