import os 
import re
import json
from dotenv import load_dotenv
from langchain import LLMChain
load_dotenv()

def get_llm():
    if os.getenv('LLM_SOURCE') == 'openai':
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=os.getenv('LLM_NAME'))
    elif os.getenv('LLM_SOURCE') == 'grok':
        from langchain_groq import ChatGroq
        llm = ChatGroq(groq_api_key = os.getenv('GROQ_API_KEY'), model = 'llama3-70b-8192', temperature=1)
    elif os.getenv('LLM_SOURCE') == 'anthropic':
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(model=os.getenv('LLM_NAME'))
    elif os.getenv('LLM_SOURCE') == 'huggingface':
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        llm = HuggingFaceEndpoint(repo_id=os.getenv('LLM_NAME'), task="text-generation", repetition_penalty=1.03)
    elif os.getenv('LLM_SOURCE') == 'gemini':
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model=os.getenv('LLM_NAME'))
    else:
        raise NotImplementedError("LLM Not currently supported.")
    return llm





# from langchain.agents import tool

from prompts import *

def get_question_chains(problem_type):
    """get the chain with prompts | llm
    problem_type currently support one of these:
        - multiple choice
        - True/False
        - Fill in the blank 
        - essay
        - coding
        - '' # just normal question
    """
    llm = get_llm()
    question_prompt = QuesPrompts(problem_type).prompt
    question_chain = LLMChain(llm=llm, prompt=question_prompt)
    return question_chain

def get_evaluation_chains(problem_type):
    """get the chain with prompts | llm
    problem_type currently support one of these:
        - multiple choice
        - True/False
        - Fill in the blank 
        - essay
        - coding
        - '' # just normal question
    """
    llm = get_llm()
    evaluation_prompt = EvalPrompts(problem_type).prompt
    evaluation_chain =  LLMChain(llm=llm, prompt=evaluation_prompt)
    return evaluation_chain


def get_answer_chains(problem_type):
    """get the chain with prompts | llm
    problem_type currently support one of these:
        - multiple choice
        - True/False
        - Fill in the blank 
        - essay
        - coding
        - '' # just normal question
    """
    llm = get_llm()
    answer_prompt = AnsPrompts(problem_type).prompt
    answer_chain = LLMChain(llm=llm, prompt=answer_prompt)
    return answer_chain



def get_answer_chain_with_tool(problem_type):
    assert problem_type=='coding'

    from pydantic.v1 import BaseModel, Field
    from langchain.utils.openai_functions import convert_pydantic_to_openai_function
    from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser, JsonKeyOutputFunctionsParser

    class MODELWITHTOOL(BaseModel):
        """Overview of a section of text."""
        code: str = Field(description="Retrieve answer code.")
        unit_test_code: str = Field(description="Retrieve unit test code.")
        # explanation: str = Field( description=".")
        language: str = Field(description="Retrieve the programming language.")

    # Convert the tag to openai functions
    overview_tagging_function = [
        convert_pydantic_to_openai_function(MODELWITHTOOL)
    ]
    llm = get_llm()
    # the tagged model
    tagging_model = llm.bind(
        functions=overview_tagging_function,
        function_call={"name":"MODELWITHTOOL"}
    )

    answer_prompt = AnsPrompts('coding').prompt

    tagging_chain = answer_prompt | tagging_model | JsonOutputFunctionsParser()
    return tagging_chain


if __name__ == '__main__':
    from llm_agent import ai_question, ai_answer_code
    question = ai_question('software engineer', 'difficult', 'programming', 'coding')['question']
    tagging_chain = get_answer_chains("")#get_answer_chain_with_tool()
    ans = tagging_chain.invoke({"question": question, "history": ""})
    