#You may need to install PyPDF2 into your environment, run:
#pip install PyPDF2
import PyPDF2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

def extract_text_from_pdf(input_pdf_path, output_txt_path):
    try:
        with open(input_pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            if len(pdf_reader.pages) == 0:
                print("The PDF file is empty.")
                return

            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()

        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text_content)

        print(f"Text content extracted from '{input_pdf_path}' and saved to '{output_txt_path}'.")

    except FileNotFoundError:
        print("Error: The specified PDF file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
input_pdf_path = filedialog.askopenfilename()

output_txt_path = 'output.txt'  # Replace 'output.txt' with the desired output text file path
extract_text_from_pdf(input_pdf_path, output_txt_path)
