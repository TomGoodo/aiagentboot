import os, subprocess
from google.genai import types
def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
       return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(args=["python3", abs_file_path],timeout=30,capture_output=True, cwd=abs_working_dir)

        if (len(result.stdout) == 0 and len(result.stderr) == 0) or (result.stdout == None and result.stderr == None):
            output = "No output produced"
        else:
            output = f"STDOUT: {result.stdout.decode('utf-8')}, STDERR: {result.stderr.decode('utf-8')} "
        if not result.returncode == 0:
            output += f"Process exited with code {result.returncode}"
        
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the filename .py, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The File path of the python file being run.",
                ),
        },
    ),
)