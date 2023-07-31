character_limit = 1000

def split_file(filename, chunk_size=5000):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunk = []
    chunk_count = 1

    for line in lines:
        if len('\n'.join(chunk + [line])) < chunk_size:
            chunk.append(line)
        else:
            with open(f"{filename}_{chunk_count}.txt", 'w') as file:
                file.writelines(chunk)
            chunk = [line]
            chunk_count += 1

    if chunk:
        with open(f"{filename}_{chunk_count}.txt", 'w') as file:
            file.writelines(chunk)

split_file('output.txt')