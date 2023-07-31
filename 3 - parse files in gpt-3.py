import openai
import os
import glob

def api_openai(input,out_file):
    openai.api_key='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'
    #openai.api_key = os.getenv("OPENAI_KEY")
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
    out_file = f"chat_conversation.txt"
    with open(out_file,'a',encoding='utf-8',errors='ignore') as file:
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
    prompt = f"of a {len(file_list)} page document. I need you to summarise this in less than 100 words.The target audience are PHD students who understand techincal and complicated techniques Please start each respons with the part number I just gave you"
    remove_conversations()
    
    for i in range(len(file_list)):
        with open(file_list[i], 'r',encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        api_openai(f"I am passing in part {count}. {prompt}-{lines}",True)
        count+=1
            
    #cleanup output
    with open('chat_conversation.txt', 'r', encoding='utf-8',errors='ignore') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    with open('chat_conversation.txt', 'w', encoding='utf-8',errors='ignore') as file:
        file.write('\n'.join(lines))

main()