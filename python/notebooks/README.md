# RAG-Buddy Python Notebooks

Assumptions
This Quickstart assumes the following prerequisites are met:

You have an active OpenAI API key. If you do not possess one, please obtain it from [OpenAI]('https://platform.openai.com/api-keys').
Your use case involves RAG with the generation of a single citation within the response.

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
Copy the newly generated API key for use in notebook.