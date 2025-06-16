import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_path):
        f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_working_path):
        try:
                os.makedirs(abs_working_path)
        except Exception as e:
            return f"Error: creating file {e}"
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
         return f"Error: Writing File {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file that is being written.",
                ),
            "content": types.Schema(
                 type=types.Type.STRING,
                 description="The content that is being written into the file",
            ),
            
        },
    ),
)