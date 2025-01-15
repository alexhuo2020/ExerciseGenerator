# ExerciseGenerator: A Problem Generator Powered by AI

This repository contains the frontend and backend code for a problem generator app with ReactJS and Flask.

To run the frontend on localhost, run 
```bash
cd ./exercisegenerator/frontend/exercisegenerator-app/
npm install
npm start
```

To run the backend on localhost, run
```bash
cd ./backend
touch .env
```
Modify the `.env` file with 
```
LLM_SOURCE=openai or gemini or grok or anthropic or huggingface
LLM_NAME= the name of the llm you want to use
GROQ_API_KEY=YOUR_API_KEY
GOOGLE_API_KEY=YOUR_API_KEY
OPENAI_API_KEY=YOUR_API_KEY
GEMINI_API_KEY=YOUR_API_KEY
```
Just update the model and API key you want to use. To get a free api key, one can use the Llama Grok API key (
https://console.groq.com/keys) or the Gemini API key (https://ai.google.dev/gemini-api/). Note that these APIs have limited usage in terms on tokens and model types. One can also obtains paid API via them and also openai, anthropic or other large language model API providers. Since we use LangChain, it is easy to modify the function `get_llm` in file `backend/llm_chains` to support all the models that LangChain supports.


then run
```bash
python main.py
```

Feel free to modify the code and add new features and components. 


Enjoy!