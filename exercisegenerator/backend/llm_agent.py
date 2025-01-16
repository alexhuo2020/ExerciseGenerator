from llm_chains import get_llm, get_question_chains, get_answer_chains, get_evaluation_chains, get_answer_chain_with_tool
import re
from utils import save_code_from_markdown_to_file, execute_generated_code, save_code, save_code_from_human_input

def ai_question(character_name, expert_name, game_name, level, problem_type=''):
    print('problemType', problem_type)
    question_chain = get_question_chains(problem_type)
    history = []
    question = question_chain.invoke({"character_name": character_name, "expert_name": expert_name, "game_name": game_name, "type": type, "level":level})['text']
    question = question.replace("\n\n","\n")
    history.append(f"AI: {question}")
    return {'history': history, 'question': question} 


def ai_answer(question, history, human_answer='', problem_type=''):
    answer_chain = get_answer_chains(problem_type)
    history.append(f"You: {human_answer}")
    ans = answer_chain.invoke({"question": question, "history": "\n".join(history)})['text']
    history.append(f"AI: {ans}")
    return {'answer': ans, 'history': history}

def ai_evaluation(question, history, human_answer, problem_type=''):
    evaluation_chain = get_evaluation_chains(problem_type)
    history.append(f"You: {human_answer}")
    evaluation = evaluation_chain.invoke({"question": question, "human_answer": human_answer, "history": "\n".join(history)})['text']
    history.append(f"AI Evaluation: {evaluation}")
    score = int(re.findall(r'[sS]core:\s[0-9]+', evaluation)[0].split(" ")[-1])
    return {'history':history, 'score': score, 'evaluation': evaluation}

def ai_evaluation_code(question, history, human_answer, problem_type='', language = 'python', percentage_of_run = 0.5 ):
    evaluation_chain = get_evaluation_chains(problem_type)
    history.append(f"You: {human_answer}")
    evaluation = evaluation_chain.invoke({"question": question, "human_answer": human_answer, "history": "\n".join(history)})['text']
    history.append(f"AI Evaluation: {evaluation}")
    script = save_code_from_human_input(human_answer, language)
    code_run_output = execute_generated_code(script, language).get('output', '')
    if 'passed' not in code_run_output:
        score_for_run = 0
    else:
        score_for_run = 10
    score = int(re.findall(r'[sS]core:\s[0-9]+', evaluation)[0].split(" ")[-1])
    score = percentage_of_run * score_for_run + (1.0 - percentage_of_run) * score
    return {'history':history, 'score': score, 'evaluation': evaluation}




def ai_answer_code(question, history, human_answer='', problem_type='coding', max_trial=2):
    answer_chain = get_answer_chains(problem_type)
    history.append(f"You: {human_answer}")
    code_run_output = ''
    status = True 
    repeat = 0
    if ('passed' not in code_run_output)  and repeat != 2:
        ans = answer_chain.invoke({"question": question, "history": "\n".join(history)})['text']
        script, language = save_code_from_markdown_to_file(ans)
        language = language if language!='' else 'python'
        code_run_output = execute_generated_code(script, language, is_unit_test=True).get('output', '')
        repeat += 1
    history.append(f"AI: {ans}")
    if not ('passed' in code_run_output):
        status = False # the AI answer is wrong

    return {'answer': ans, 'history': history, 'status': status}


def ai_answer_code_with_tool(question, history, human_answer='', problem_type='coding', max_trial=2):
    answer_chain = get_answer_chain_with_tool(problem_type)
    history.append(f"You: {human_answer}")
    code_run_output = ''
    status = True 
    repeat = 0
    if code_run_output != 'All tests passed!\n' and repeat != 2:
        ans = answer_chain.invoke({"question": question, "history": ""})
        script, language = save_code(ans['code'], ans['unit_test_code'], ans['language'])
        code_run_output = execute_generated_code(script, language, is_unit_test=True).get('output', '')
        repeat += 1
    history.append(f"AI: {ans}")
    if code_run_output != 'All tests passed!\n':
        status = False # the AI answer is wrong

    return {'answer': ans['code'], 'history': history, 'status': status}
