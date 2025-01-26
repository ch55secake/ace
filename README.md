## ace

Reach out to the OpenAI API from the commandline. 

### Getting started

Before you can use the normal query functionality, you need to have a valid OpenAI api key and once you have that 
you will need to run: 

```bash
 ace init <api-key> <filepath-optional>
```

If you do not provide a path for the yaml configuration file to live it will default to `$HOME/.config/ace/config.yaml`. 
Once you have this file the tool will always read from there when making requests to the api. 

### Usage 

> [!NOTE]
> Price per request may vary on which model you choose to use, reasoning models are at the moment
> the most expensive models you can choose. See [here](https://platform.openai.com/docs/pricing) for more information.

To run a query and get a response, you can use this command: 

```
 ace ask 'Write me a for loop in python'
```

Here is what the output will look like: 

Certainly! Here's a simple for loop in Python that prints the numbers from 1 to 5:
```python
for i in range(1, 6):   
  print(i)
```

It will render the response to the query in markdown inside the terminal like the above. 
You can use a different model from one of the many available. To see the available list of models,
you can run:
```
 ace models 
```
This will output: 
```
Here is the list of models currently supported by open ai:
 - gpt-4o-audio-preview-2024-10-01
 - gpt-4o-mini-audio-preview
 - gpt-4o-realtime-preview.......
```
You can then pick one of these models and use it in your queries with the `--model` flag. 
