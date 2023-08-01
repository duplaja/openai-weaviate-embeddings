#!/usr/bin/env python3
import weaviate

client = weaviate.Client(
    url="http://0.0.0.0:9000",  # Replace with your endpoint
)

## Uncomment to Delete the Schema, by name. Useful if you need to drop / recreate

# client.schema.delete_class("School")


class_obj = {
    "class": "School",
    "description": "School Document for Analysis", 
    "vectorIndexConfig": {
        "distance": "cosine",
    },
    "moduleConfig": {
        "generative-openai": {
          "model": "gpt-4",             #As far as I know, you cannot change this once created.    
          "maxTokensProperty": 3000, 
        }
    },
    "properties": [
        {
            "dataType": ["text"],
            "description": "Type of document: administrative, personal, student, other",
            "moduleConfig": {
                "text2vec-openai": {
                "skip": True,
                "vectorizePropertyName": False
                }
            },
            "name": "document_type",
        },
        {
            "dataType": ["int"],
            "description": "Year the document was created.",
            "moduleConfig": {
                "text2vec-openai": {
                "skip": True,
                "vectorizePropertyName": False
                }
            },
            "name": "year",
        },
        {
            "dataType": ["text"],
            "description": "Document Title",
            "moduleConfig": {
                "text2vec-openai": {
                "skip": True,
                "vectorizePropertyName": False
                }
            },
            "name": "title",
        },
        {
            "dataType": ["text"],
            "description": "The author",
            "moduleConfig": {
                "text2vec-openai": {
                "skip": True,
                "vectorizePropertyName": False
                }
            },
            "name": "author",
        },
        {
            "dataType": ["text"],
            "description": "Text Chunk Content",
            "moduleConfig": {
                "text2vec-openai": {
                "skip": False,
                "vectorizePropertyName": False
                }
            },
            "name": "content",
        },
    ],
    "vectorizer": "text2vec-openai",
}

# Add the class to the schema, creates it in your Weaviate database. Only need to run once per class
client.schema.create_class(class_obj)

# Get the schema
#schema = client.schema.get()

# Print the schema
#print(json.dumps(schema, indent=4))
