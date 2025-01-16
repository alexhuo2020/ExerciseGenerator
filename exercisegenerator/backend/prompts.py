from langchain_core.prompts import PromptTemplate

class QuesPrompts():
    def __init__(self, type = ''):
        self.type = type
        if self.type == '':
            # Define the prompt for generating questions with history
            self.prompt = PromptTemplate(
                input_variables=["character_name", "expert_name", "game_name", "level", "type", "history"],
                template= """You are {expert_name}. Please provide one {level} {type} problem about {game_name} each time randomly and ask me who is a {character_name} to provide the answer. Only output the question and answer choices without any additional text, explanations, greetings, or introductions. Do not provide the solution unless explicitly asked. Start the response with Problem directly."
                """
                )
        elif self.type == 'coding':
            self.prompt = PromptTemplate(
                input_variables=["role", "level", "topic", "type", "history"],
                template= """You are a professional {expert_name} and you know how to solve problems effectively and efficiently. Please provide one {level} {game_name} {type} problem each time randomly and ask the students who is a {character_name} to provide the code. Provide code for the function name and variables. Do not provide solution until you are asked to provide the solution.  Use `\`\`\`language\n` for coding blocks if it exists with language being the programming language. Start the response with Problem directly.\n 
                """
                )
        else:
            self.prompt = PromptTemplate(
                input_variables=["character_name", "expert_name", "game_name", "level", "type", "history"],
                template= """You are {expert_name}. Please provide one {level} {type} problem about {game_name} each time randomly and ask me who is a {character_name} to provide the answer. Only output the question and answer choices without any additional text, explanations, greetings, or introductions. Do not provide the solution unless explicitly asked. Start the response with Problem directly."
                """
                )

class EvalPrompts():
    def __init__(self, type = ''):
        self.type = type 
        if self.type == '':
            self.prompt = PromptTemplate(
                input_variables=["question", "human_answer", "history"],
                template="""
                Based on the previous conversation: {history}
                Question: {question}
                Human Answer: {human_answer}
                
                Check the answer. Provide feedback and a score from 0 to 10 using 'score:'. If it is correct, give 10.
                If the score is below 7, suggest improvements or provide a hint to help the user enhance their answer.
                Do not provide the correct answer.
                """
            )
        elif self.type == 'coding':
            self.prompt = PromptTemplate(
                input_variables=["question", "human_answer", "history"],
                template="""
                Based on the previous conversation: {history}
                Question: {question}
                Human Answer: {human_answer}
                
                Evaluate the answer based on clarity, correctness, and depth. Provide feedback and a score from 0 to 10 using 'Score:'. If it is correct give 10.
                If the score is below 7, suggest improvements or provide a hint to help the user enhance their answer.
                Do not provide the correct answer.
                """
            )
        else:
            self.prompt = PromptTemplate(
                input_variables=["question", "human_answer", "history"],
                template="""
                Based on the previous conversation: {history}
                Question: {question}
                Human Answer: {human_answer}
                
                Check the answer. Provide feedback and a score from 0 to 10 using 'score:'. If it is correct, give 10.
                If the score is below 7, suggest improvements or provide a hint to help the user enhance their answer.
                Do not provide the correct answer.
                """
            )


class AnsPrompts():
    def __init__(self, type = ''):
        self.type = type 
        if self.type == '':
            self.prompt = PromptTemplate(
                input_variables=["question", "history"],
                template="Based on the history: {history}. Provide the correct answer and an explanation for the following problem: {question}"
            )
        elif self.type == 'coding':
            self.prompt = PromptTemplate(
                input_variables=["question", "history"],
                template="Based on the history: {history}. Provide the correct code, unit test code and an explanation for the following problem: {question} in three different blocks.\n code: ...\n unit test code: \n explanation:\n "
            )
        else:
            self.prompt = PromptTemplate(
                input_variables=["question", "history"],
                template="Based on the history: {history}. Provide the correct answer and an explanation for the following problem: {question}"
            )

class TutPrompts():
    def __init__(self, type = ''):
        self.type = type
            # Define the prompt for generating questions with history
        self.prompt = PromptTemplate(
            input_variables=["character_name", "expert_name", "game_name"],
            template= """You are {expert_name} and I am {character_name}. Please provide a comprehensive tutorial about {game_name}.
            """
            )