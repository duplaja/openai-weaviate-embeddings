# Openai + Weaviate Embeddings

Collection of tools for using OpenAI + Weaviate (vector DB) to create searchable document databases.

1) Sign up for OpenAI, and get your API Key

2) Set up Weaviate database. I'm just going to do the basics here: run with docker, localhost, no authentication. [See Weaviate docs for all possibilities.](https://weaviate.io/developers/weaviate/installation). I'll include my `docker-compose.yml` file. I bind to port 9000 on the local machine. You will need to set your own OpenAI key here. I've included some basic modules for working with OpenAI, but [there are others, including backups, etc.](https://weaviate.io/developers/weaviate/configuration/backups)

3) Install the Python client library for Weaviate (Python 3.7+) with `pip install weaviate-client`

4) Create a schema class. [See detailed instructions here.](https://weaviate.io/developers/weaviate/configuration/schema-configuration) See `manage-classes.py` for some basic example code and a sample class.
  
   **Note:** Some aspects of this class are immutable, so if you want to make a change, you're likely going to have to delete and re-create it, including re-inserting / vectorizing all data again. Make sure this is how you want, and test with a small dataset first.

      **Note:** The module config back when we created the class is, as far as I know, immutable. If I find a way to change it, I'll update here. That means you're stuck with gpt-3.5-turbo or gpt-4, unless you pull the matching embeddings yourself and build the OpenAI query yourself (out of scope of this repo). Consider carefully, and I suggest testing with a smaller dataset.

5) Insert some data. You'll want to [create objects and batch insert them.](https://weaviate.io/developers/weaviate/manage-data/import). See `chunk-for-vectors.py` for some code that takes a single text file, chunks it, and then inserts it into the database. As long as we have `text2vec-openai` module configured correctly (in docker-compose as DEFAULT_VECTORIZER_MODULE), OpenAI will automatically be called to embed / vectorize the data as it is inserted.

6) Query the data. This uses GraphQL. It gets all `n` most similar items, then feeds it back into OpenAI to get a response. You can either do a Task, or a Prompt. Prompt returns the OpenAI interpretation for each item, while Task returns it for all the items in aggregate. [See Detailed Information Here](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai). You can see some sample code in `query-data.py`
