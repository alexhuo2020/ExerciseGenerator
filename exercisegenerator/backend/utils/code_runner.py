import subprocess
import subprocess
import os

def execute_generated_code(generated_code_file: str, language='python', is_unit_test=False):
    """
    Executes the code provided in the generated_code_file in the specified programming language.
    If the file is a unit test, it will execute it using the appropriate test framework.

    Args:
        generated_code_file (str): The path to the file containing the code to execute.
        language (str): The programming language to execute the code in. Default is 'python'.
        is_unit_test (bool): If True, the file is a unit test file. Default is False.

    Returns:
        dict: A dictionary with 'output' as the result of the code execution, or 'error' if an exception occurs.
    """
    try:
        print(language)
        # Check if it's a unit test file and handle accordingly
        if  not is_unit_test:
            # Handle normal code execution (non-unit-test files)
            if language == 'python':
                result = subprocess.run(['python3', generated_code_file], capture_output=True, text=True)
            
            elif language == 'cpp':
                execfile = ''.join(generated_code_file.split(".")[:-1])+ '.o'
                subprocess.run(['g++',generated_code_file, '-o', execfile])
                result = subprocess.run(execfile, capture_output=True, text=True)


            elif language == 'c':
                execfile = ''.join(generated_code_file.split(".")[:-1])+ '.o'
                subprocess.run(['gcc',generated_code_file, '-o', execfile])
                result = subprocess.run(execfile, capture_output=True, text=True)

            elif language == 'javascript':
                result = subprocess.run(['node', generated_code_file], capture_output=True, text=True)
            
            elif language == 'ruby':
                result = subprocess.run(['ruby', generated_code_file], capture_output=True, text=True)
            
            elif language == 'java':
                result = subprocess.run(['java', generated_code_file], capture_output=True, text=True)
            
            elif language == 'bash':
                result = subprocess.run(['bash', generated_code_file], capture_output=True, text=True)

            elif language == 'go':
                result = subprocess.run(['go', 'run', generated_code_file], capture_output=True, text=True)

            elif language == 'php':
                result = subprocess.run(['php', generated_code_file], capture_output=True, text=True)

            elif language == 'swift':
                result = subprocess.run(['swift', generated_code_file], capture_output=True, text=True)

            elif language == 'rust':
                result = subprocess.run(['cargo', 'run'], capture_output=True, text=True)

            elif language == 'scala':
                result = subprocess.run(['scala', generated_code_file], capture_output=True, text=True)

            elif language == 'typescript':
                result = subprocess.run(['ts-node', generated_code_file], capture_output=True, text=True)

            elif language == 'sql':
                # SQL code execution using PostgreSQL client (psql)
                result = subprocess.run(['psql', '-f', generated_code_file], capture_output=True, text=True)

            else:
                # Unsupported language
                raise NotImplementedError(f"Language {language} is not supported.")
        else:
            if language == 'python':
                # Run Python unit tests with pytest
                result = subprocess.run(['pytest', generated_code_file], capture_output=True, text=True)
            

            elif language == 'cpp':
                execfile = ''.join(generated_code_file.split(".")[:-1])+ '.o'
                subprocess.run(['g++',generated_code_file, '-o', execfile])
                result = subprocess.run(execfile, capture_output=True, text=True)


            elif language == 'c':
                execfile = ''.join(generated_code_file.split(".")[:-1])+ '.o'
                subprocess.run(['gcc',generated_code_file, '-o', execfile])
                result = subprocess.run(execfile, capture_output=True, text=True)

            elif language == 'javascript':
                # Run JavaScript unit tests with Jest (or Mocha, Chai, etc.)
                result = subprocess.run(['npx', 'jest', generated_code_file], capture_output=True, text=True)
            
            elif language == 'ruby':
                # Run Ruby unit tests with RSpec
                result = subprocess.run(['rspec', generated_code_file], capture_output=True, text=True)
            
            elif language == 'java':
                # Run Java unit tests with Maven or Gradle (assumes compiled code)
                result = subprocess.run(['mvn', 'test', '-Dtest=' + generated_code_file], capture_output=True, text=True)
            
            elif language == 'bash':
                # Bash doesn't typically have unit tests, but we can execute any test scripts directly
                result = subprocess.run(['bash', generated_code_file], capture_output=True, text=True)

            elif language == 'go':
                # Run Go unit tests with the Go test framework
                result = subprocess.run(['go', 'test', generated_code_file], capture_output=True, text=True)

            elif language == 'php':
                # Run PHP unit tests with PHPUnit
                result = subprocess.run(['php', './vendor/bin/phpunit', generated_code_file], capture_output=True, text=True)
            
            elif language == 'swift':
                # Run Swift tests with Swift Package Manager (SPM)
                result = subprocess.run(['swift', 'test', '--package-path', generated_code_file], capture_output=True, text=True)

            elif language == 'rust':
                # Run Rust tests with Cargo
                result = subprocess.run(['cargo', 'test'], capture_output=True, text=True)

            elif language == 'scala':
                # Run Scala tests with sbt (Scala Build Tool)
                result = subprocess.run(['sbt', 'test'], capture_output=True, text=True)

            elif language == 'typescript':
                # Run TypeScript unit tests with Jest
                result = subprocess.run(['npx', 'jest', generated_code_file], capture_output=True, text=True)

            elif language == 'sql':
                # SQL doesn't have unit tests, execute SQL queries directly
                result = subprocess.run(['psql', '-f', generated_code_file], capture_output=True, text=True)

            else:
                # Unsupported language for unit tests
                raise NotImplementedError(f"Unit tests for {language} are not supported.")

        
        
        # Check if the code execution produced output or error
        if result.returncode == 0:
            return {"output": result.stdout, "std_err": result.stderr}
        else:
            return {"error": result.stderr}
    
    except Exception as e:
        raise NotImplementedError("Error")
        # Return the error message in case of an exception
        # return {"error": "Not Implemented"}


# def execute_generated_code(generated_code_file: str, language = 'python'):
#     """
#     Executes the code provided in the generated_code string.
    
#     Args:
#         generated_code (str): The code to execute as a string.
    
#     Returns:
#         dict: A dictionary with 'output' as the result of the code execution, or 'error' if an exception occurs.
#     """
#     language_runs = ['python3', 'node', 'ruby', 'java', 'bash', '']
#     try:
#         # Define a local namespace for executing the code safely
#         local_namespace = {}
#         # Execute the code in the local namespace
    
#         local_namespace = subprocess.run([language_run, generated_code_file],capture_output=True, text=True)
#         # exec(generated_code, {}, local_namespace)
#         print(local_namespace)
#         # Return the result of the code if there is one in local_namespace
#         return {"output": local_namespace.stdout, "std_err": local_namespace.stderr}
#     except Exception as e:
#         # Return the error message in case of an exception
#         return {"error": str(e)}






import os

def execute_code_from_repo(repo_files: dict, main_script: str):
    """
    Executes code from a repository structure represented by a dictionary of file names and their contents.

    Args:
        repo_files (dict): A dictionary where keys are file paths (str) and values are code contents (str).
        main_script (str): The main script file name to execute as the entry point.

    Returns:
        dict: A dictionary with 'output' for successful execution or 'error' in case of an exception.
    """
    repo_dir = 'temp_repo'
    
    # Step 1: Create the repository directory
    os.makedirs(repo_dir, exist_ok=True)
    
    try:
        # Step 2: Write each file to the directory
        for file_path, code_content in repo_files.items():
            full_path = os.path.join(repo_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(code_content)
        
        # Step 3: Set up execution context by loading files dynamically
        execution_globals = {"__name__": "__main__"}
        # Step 4: Execute each file in the order needed (if known), or directly execute the main script
        main_script_path = os.path.join(repo_dir, main_script)
        with open(main_script_path, 'r') as file:
            main_code = file.read()
        import subprocess
        a = subprocess.run(['python3', main_script_path],capture_output=True, text=True)
        return a.stdout
    
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Cleanup can be added here if needed to remove the `repo_dir`
        pass

if __name__ == '__main__':
    # Execute the generated code
    

    # Example usage
    result = execute_generated_code('')
    print(result)


    # Example usage
    repo_files = {
        "module1.py": "def greet(): return 'Hello from module1!'",
        "module2.py": "def welcome(): return 'Welcome from module2!'",
        "main.py": "from module1 import greet\nfrom module2 import welcome\nprint(greet())\nprint(welcome())"
    }
    result = execute_code_from_repo(repo_files, main_script="main.py")
    print(result)

