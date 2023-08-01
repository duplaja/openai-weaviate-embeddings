#!/usr/bin/env python3

import weaviate
from langchain.text_splitter import CharacterTextSplitter
import json


## Loads single text file to variable.
def load_file_content(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

## Chunks text. Adjust chunk_size as needed. This is more of a guideline. Splits by paragraphs right now.
def chunk_text(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n\n",
        chunk_size = 256,
        chunk_overlap  = 20
    )
    docs = text_splitter.create_documents([text])
    return docs
    
client = weaviate.Client(
    url="http://0.0.0.0:9000",  # Replace with your endpoint
)


classname = "School" #Set to the classname you created previously.

text = load_file_content('Handbook 23-24.txt') #Name of a text file to import

docs = chunk_text(text)

with client.batch(
    batch_size=100,  # Specify the batch size
    num_workers=2,   # Parallelize the process
) as batch:

    for document in docs:

        #fill in any property fields you created originally in your class.
        
        data_obj={
            'document_type': 'administrative',
            'year': 2023,
            'title' : 'Handbook 23-24',
            'author' : 'admin',
            'content' : document.page_content  #From the splitter above.
        }

        batch.add_data_object(
            data_obj,
            classname,
            # tenant="tenantA"  # If multi-tenancy is enabled, specify the tenant to which the object will be added.
        )
