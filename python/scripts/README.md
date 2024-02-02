# RAG-Buddy Python Scripts

Assumptions
This Quickstart assumes the following prerequisites are met:

You have an active OpenAI API key. If you do not possess one, please obtain it from [OpenAI]('https://platform.openai.com/api-keys').
You are using the OpenAI Python client. Installation and setup instructions can be found in the repository.
Your use case involves RAG with the generation of a single citation within the response.

Python and pip installed in your system.
Pipenv installed, if not execute $ pip install virtualenv

Activate the virtualenv using $ pipenv shell

Download the necessary packages using $ pipenv install

Create a Cache
To begin using RAG-Buddy, a new project must be created. If you haven’t set up a project yet, follow these steps:

Visit the [RAG-Buddy Dashboard]('https://rag-buddy.dev.helvia.ai/login') at RAG-Buddy Dashboard and sign up for an account if you don’t already have one.

Once you’re signed in:

On your dashboard, click [Create a new project].
Name your project.
Select OpenAI:ADA2 as your embedding model.
Select OpenAI Chat Completions API as your LLM provider.
Select the 'RAG' cache type
Click Create Project to create your project.
Next, you’ll need an API key for your cache:

Navigate to the Services tab.
Scroll down to the API Keys for Cache section.
Click on Create new key.
Assign a name to your key and select Create API Key.
Copy the newly generated API key for use in the next step.

Navigate to the .env file and fill in the OPENAI_API_KEY and RAG_BUDDY_KEY

To execute the script navigate to the python/scripts directory and execute $ python RAG-Buddy-integration.py