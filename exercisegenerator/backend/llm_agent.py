from llm_chains import get_llm, get_question_chains, get_answer_chains, get_evaluation_chains, get_answer_chain_with_tool
import re
from utils import save_code_from_markdown_to_file, execute_generated_code

def ai_question(character_name, expert_name, game_name, level, problem_type=''):
    question_chain = get_question_chains(problem_type)
    history = []
    question = question_chain.invoke({"character_name": character_name, "expert_name": expert_name, "game_name": game_name, "type": type, "level":level})['text']
    question = question.replace("\n\n","\n")
    history.append(f"AI: {question}")
    return {'history': history, 'question': question} 

def ai_answer(question, history, problem_type=''):
    answer_chain = get_answer_chains(problem_type)
    ans = answer_chain.invoke({"question": question, "history": "\n".join(history)})['text']
    history.append(f"AI: {ans}")
    return {'answer': ans, 'history': history}

# def ai_answer(question, history, human_answer, problem_type=''):
#     answer_chain = get_answer_chains(problem_type)
#     history.append(f"You: {human_answer}")
#     ans = answer_chain.invoke({"question": question, "history": "\n".join(history)})['text']
#     history.append(f"AI: {ans}")
#     return {'answer': ans, 'history': history}

def ai_evaluation(question, history, human_answer, problem_type=''):
    evaluation_chain = get_evaluation_chains(problem_type)
    history.append(f"You: {human_answer}")
    evaluation = evaluation_chain.invoke({"question": question, "human_answer": human_answer, "history": "\n".join(history)})['text']
    history.append(f"AI Evaluation: {evaluation}")
    score = int(re.findall(r'[sS]core:\s[0-9]+', evaluation)[0].split(" ")[-1])
    return {'history':history, 'score': score, 'evaluation': evaluation}

def ai_answer_code(question, history, human_answer, problem_type):
    answer_chain = get_answer_chains(problem_type)
    history.append(f"You: {human_answer}")
    ans = answer_chain.invoke({"question": question, "history": "\n".join(history)})['text']
    history.append(f"AI: {ans}")
    script, language = save_code_from_markdown_to_file(ans)
    language = language if language!='' else 'python'
    print(execute_generated_code(script, language))
    return {'answer': ans, 'history': history}
