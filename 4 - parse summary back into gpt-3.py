import openai
import os
import glob
from dotenv import load_dotenv
load_dotenv()

def api_openai(input,out_file):
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
    result = response.choices[0].text
    if out_file == True:
        conversation(f"{result}")
        
def conversation(text):
    out_file = f"processed_output.txt"
    with open(out_file,'a') as file:
        file.write(f"{text}")
    
def find_matching_files():
    match_pattern = 'output.txt_*.txt'
    current_dir = os.getcwd()
    matching_files = glob.glob(match_pattern)
    return matching_files

def remove_conversations():
    try:
        current_dir = os.getcwd()
        for file_name in os.listdir(current_dir):
            if 'conversation' in file_name:
                file_path = os.path.join(current_dir, file_name)
                os.remove(file_path)
    except:
        return


def main():
    count = 1
    file_list = find_matching_files()      
    prompt = f"I am going to provide text from a document that has been summarised by parts. I require you to conduct an overall summary of the text. This summary is for PHD students and should be written as a summary of text that can be reviewed as part of a study aide."
    #remove_conversations()
    
    for i in range(len(file_list)):
        with open('chat_conversation.txt', 'r',errors='ignore') as file:
            lines = file.readlines()
        api_openai(f"{prompt}\n{lines}",True)
        count+=1
            
    #cleanup output
    with open('processed_output.txt', 'r', errors='ignore') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    with open('processed_output.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

main()