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
        with open(f"{filename}_{chunk_count}.txt", 'w') as file:
            file.writelines(chunk)

split_file('output.txt')