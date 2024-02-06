# RAG-Buddy Python Scripts

Assumptions
This Quickstart assumes the following prerequisites are met:

You have an active OpenAI API key. If you do not possess one, please obtain it from [OpenAI]('https://platform.openai.com/api-keys').
You are using the OpenAI Python client. Installation and setup instructions can be found in the repository.
Your use case involves RAG with the generation of a single citation within the response.

Python and pip installed in your system.
pipenv installed, if not execute $ pip install pipenv

Download the necessary packages and create the pipenv using $ pipenv install

Activate the pipenv using $ pipenv shell

Create a Cache
To begin using RAG-Buddy, a new project must be created. If you haven’t set up a project yet, follow these steps:

Visit the [RAG-Buddy Console]('https://www.ragbuddy.ai/') and sign up for an account if you don’t already have one.

Once you’re signed in:

On your console, click [Create a new project].
Name your project.
Select OpenAI:ADA2 as your embedding model.
Select OpenAI Chat Completions API as your LLM provider.
Select the 'RAG+Citation' cache type.
Click Create Project to create your project.
Next, you’ll need an API key for your cache:

Navigate to the Services tab.
Scroll down to the API Keys for Cache section.
Click on Create new key.
Assign a name to your key and select Create API Key.
Copy the newly generated API key for use in the next step.

Navigate to the .env.sample file and create a copy called .env . Fill in required environmental variables.

To execute the script navigate to the python/scripts directory and execute $ python rag-buddy-ragc-proxy.py or execute $ python -m python.scripts.rag-buddy-ragc-proxy 
To execute the script navigate to the python/scripts directory and execute $ python RAG-Buddy-integration.py


## rag-buddy-ragc-proxy

Use python ragc_api_client.py --help to display the script's usage information:

To execute the script use $ python -m python.scripts.ragc_api_client  "Credit card not valid anymore?" "./utils/articles/articles.txt" --cache-control  no-store
