import re 
import os 
folder = '../cache/'

def save_code(code, test_code, language):
    language_extensions = {'python': '.py', 'cpp': '.cpp', 'cshapr': '.cs', 'javascript': '.js', 'java': '.java', 'c': '.c','':'.py'}
    ext = language_extensions[language]
    with open(folder + 'ans' + ext, 'w') as f:
        f.write(code)
        f.write("\n")
        f.write(test_code)
    return folder + 'ans' + ext, language



def get_code_from_markdown(text):
    pattern = r'^```(\w+)?\s*\n(.*?)(?=^```)```'
    result = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
    return result


def save_code_from_markdown_to_file(text):
    pattern = r'^```(\w+)?\s*\n(.*?)(?=^```)```'
    result = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
    language_extensions = {'python': '.py', 'cpp': '.cpp', 'cshapr': '.cs', 'javascript': '.js', 'java': '.java', 'c': '.c','':'.py'}

    ext = language_extensions[result[0][0]]
    # if ext == '':
    #     ext = '.py'

    open(folder + 'ans' + ext, 'w').close()
    for res in result:

        with open(folder + 'ans' + ext, 'a+') as f:
            f.write(res[1])

        with open(folder + 'test' + ext, 'w') as f:
            # f.write('from ans import *')
            f.write(res[1])
    return folder + 'ans' + ext, result[0][0]

def save_code_from_human_input(human_answer, language):
    language_extensions = {'python': '.py', 'cpp': '.cpp', 'cshapr': '.cs', 'javascript': '.js'}
    ext = language_extensions[language]
    with open(folder + 'test' + ext, 'r') as f:
        # f.write('from ans import *')
        test_content = f.read()
    with open(folder + 'human_ans' + ext, 'w') as f:
        f.write(human_answer)
        f.write(test_content)
    return folder + 'human_ans' + ext
    

def run_unit_test(language):
    language_extensions = {'python': '.py', 'cpp': '.cpp', 'cshapr': '.cs', 'javascript': '.js', '':'.py'}
    ext = language_extensions[language]
    if language == '':
        language = 'python'

    from .code_runner import execute_generated_code 
    result_human = execute_generated_code(folder + 'human_ans' + ext, language)
    result_ai = execute_generated_code(folder + 'ans' + ext, language)
    print(result_human, result_ai)
    
    

