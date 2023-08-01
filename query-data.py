#!/usr/bin/env python3
import weaviate
import json

client = weaviate.Client(
    url="http://0.0.0.0:9000",  # Replace with your endpoint
)

classname = "School" # Class Name we previously created

# instruction for the generative module
generateTask = "What happens if I'm late? Ignore infromation about sports, and reply concisely" #For Tasks

#generatePrompt = "What are the consequences of tardies, from the following paragraph: {content}" #For Prompts

result = (
  client.query
  .get(classname, ["content"])
  .with_generate(grouped_task=generateTask) #Used for Tasks (aggregate)
  #.with_generate(single_prompt=generatePrompt) #Used for Single Prompts (multiple)
  .with_near_text({
    "concepts": ["being late","tardy"] #For now, I set these manually. Will come up with a better way of handling.
  })
  .with_limit(10) #Set limit of chunks to return
).do()

## See more query information here, like filtering results: https://weaviate.io/developers/weaviate/tutorials/query

#print(json.dumps(result, indent=4))

#For Tasks (aggregate). Might need to modify for Prompts
response = result['data']['Get']['School'][0]["_additional"]['generate']['groupedResult'] 

print(response)
