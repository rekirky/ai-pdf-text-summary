#You may need to install PyPDF2 into your environment, run:
#pip install PyPDF2
import PyPDF2
import tkinter as tk
import openai
import os
import glob
from dotenv import load_dotenv
from tkinter import filedialog

load_dotenv()
root = tk.Tk()
root.withdraw()

#################################
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

    except FileNotFoundError:
        print("Error: The specified PDF file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#################################
def split_file(filename, chunk_size=3000):
    with open(filename, 'r',errors="ignore") as file:
        lines = file.readlines()
    chunk = []
    chunk_count = 1
    for line in lines:
        add=''
        if chunk_count < 10:
            add=0
        if len('\n'.join(chunk + [line])) < chunk_size:
            chunk.append(line)
        else:
            with open(f"{filename}_{add}{chunk_count}.txt", 'w') as file:
                file.writelines(chunk)
            chunk = [line]
            chunk_count += 1
    if chunk:
        with open(f"{filename}_{add}{chunk_count}.txt", 'w') as file:
            file.writelines(chunk)

#################################
def api_openai(input):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    engine_list = openai.Engine.list() 
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return(response.choices[0].text)

################################# 
def conversation(text,out_file):
        with open(out_file,'a',encoding='utf-8',errors='ignore') as file:
            file.write(f"{text}")
    
#################################    
def find_matching_files():
    match_pattern = 'output.txt_*.txt'
    current_dir = os.getcwd()
    matching_files = glob.glob(match_pattern)
    return matching_files

#################################
def remove_conversations():
    try:
        current_dir = os.getcwd()
        for file_name in os.listdir(current_dir):
            if 'conversation' in file_name:
                file_path = os.path.join(current_dir, file_name)
                os.remove(file_path)
    except:
        return

#################################
def api_first():
    count = 1
    file_list = find_matching_files()      
    prompt = f"of a {len(file_list)} page document. I need you to summarise this in less than 100 words.The target audience are PHD students who understand techincal and complicated techniques Please start each respons with the part number I just gave you"
    remove_conversations()
    
    for i in range(len(file_list)):
        with open(file_list[i], 'r',encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        text = api_openai(f"I am passing in part {count}. {prompt}-{lines}")
        conversation(text,"chat_conversation.txt")
        count+=1
            
    #cleanup output
    with open('chat_conversation.txt', 'r', encoding='utf-8',errors='ignore') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    with open('chat_conversation.txt', 'w', encoding='utf-8',errors='ignore') as file:
        file.write('\n'.join(lines))

#################################
def api_second():
    prompt = f"I am going to provide text from a document that has been summarised by parts. I require you to conduct an overall summary of the text. This summary is for PHD students and should be written as a summary of text that can be reviewed as part of a study aide."
      
    with open('chat_conversation.txt', 'r',errors='ignore') as file:
        lines = file.readlines()
    text = api_openai(f"{prompt}\n{lines}")
    conversation(text,"document_summary.txt")
      
    #cleanup output
    with open('document_summary.txt', 'r', errors='ignore') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    with open('document_summary.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

#################################
def cleanup():
    try:
        current_dir = os.getcwd()
        for file_name in os.listdir(current_dir):
            if 'output' in file_name or 'chat_conversation' in file_name:
                    file_path = os.path.join(current_dir, file_name)
                    os.remove(file_path)
    except:
        return

#################################
def main():
    # Opening PDF and converting to text
    input_pdf_path = filedialog.askopenfilename()
    extract_text_from_pdf(input_pdf_path, 'output.txt')
    
    # Split extracted text into chunks
    split_file('output.txt')
    
    # Process chunks through API
    api_first()
    api_second()
    
    # Cleanup temp files
    cleanup()

#################################
main()


