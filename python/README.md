# RAG-Buddy Python Scripts

### Assumptions
- This Quickstart assumes the following prerequisites are met:

1. You have an active OpenAI API key. If you do not possess one, please obtain it from [OpenAI]('https://platform.openai.com/api-keys').
You are using the OpenAI Python client. Installation and setup instructions can be found in the repository.
Your use case involves RAG with the generation of a single citation within the response.

2. Navigate to the python directory `cd python`

3. Python and pip installed in your system.
pipenv installed, if not execute `pip install pipenv`

4. Download the necessary packages and create the pipenv using `pipenv install`

5. Activate the pipenv using `pipenv shell`

### Create a Cache
To begin using RAG-Buddy, a new project must be created. If you haven’t set up a project yet, follow these steps:

Visit the [RAG-Buddy Console]('https://www.ragbuddy.ai/') and sign up for an account if you don’t already have one.

 1. Once you’re signed in:

    1. On your console, click [Create a new project].
    2. Name your project.
    3. Select OpenAI:ADA2 as your embedding model.
    4. Select OpenAI Chat Completions API as your LLM provider.
    5. Select the 'RAG+Citation' cache type.
    6. Click Create Project to create your project.

2. Next, you’ll need an API key for your cache:

    1. Navigate to the Services tab.
    2. Scroll down to the API Keys for Cache section.
    3. Click on Create new key.
    4. Assign a name to your key and select Create API Key.
    5. Copy the newly generated API key for use in the next step.

3. Copy the .env.sample file and create a .env by executing `cp .env.sample .env`.
Then fill in the required environmental variables.

### For more information regarding each use case, consider having a look at our [documentation]('https://docs.ragbuddy.ai').