#!/usr/bin/env python3

import weaviate
from langchain.text_splitter import CharacterTextSplitter
import json
import time

#From https://weaviate.io/developers/weaviate/modules/retriever-vectorizer-modules/text2vec-openai

def callback(batch_results: dict) -> None:

    #batch_size = 100    
    batch_target_rate = 35 #may need to edit this

    # you could print batch errors here
    time_took_to_create_batch = client.batch.batch_size * (client.batch.creation_time/client.batch.recommended_num_objects)
    
    print('.',end="")
    
    time.sleep(
        max(client.batch.batch_size/batch_target_rate - time_took_to_create_batch + 1, 0)
    )


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

startTime = time.time()

classname = "School" #Set to the classname you created previously.

text = load_file_content('Handbook 23-24.txt') #Name of a text file to import

docs = chunk_text(text)

with client.batch(
    batch_size=100,  # Specify the batch size
    num_workers=2,
    timeout_retries=5,
    dynamic=True,
    callback=callback,
    
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
print(" Done!")
result = client.query.aggregate(classname).with_meta_count().do()
print(result)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
