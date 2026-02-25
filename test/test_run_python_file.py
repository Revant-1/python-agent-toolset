from functions.run_python_file import run_python_file

def test_case(working_dir, file_path, args=None):
    print(f'run_python_file("{working_dir}", "{file_path}", args={args}):')
    result = run_python_file(working_dir, file_path, args)
    # Format result for readability
    for line in result.split('\n'):
        print(f"  {line}")
    print("-" * 40)

# 1. Successful execution (usage)
test_case("calculator", "main.py")

# 2. Execution with arguments (calculation)
test_case("calculator", "main.py", ["3 + 5"])

# 3. Running unit tests
test_case("calculator", "tests.py")

# 4. Security violation (traversal)
test_case("calculator", "../main.py")

# 5. Missing file
test_case("calculator", "nonexistent.py")

# 6. Non-python file
test_case("calculator", "lorem.txt")
