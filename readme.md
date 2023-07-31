# Project - PDF summariser

## Goal - run a pdf file through AI and create a summary of the file.

### Process
1 - Open a PDF file and convert it to text
2 - Open text file and convert into 3000-character 'chunks' (3000 because of API file length limits - we need a response value as well as input)
3 - Feed each chunk into OpenAI through API and get a summary of that chunk
4 - Feed all summaries back into OpenAI and create a singular summary of the document
