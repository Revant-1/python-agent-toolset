from functions.get_file_content import get_file_content

def test_case(working_dir, file_path):
    print(f'get_file_content("{working_dir}", "{file_path}"):')
    result = get_file_content(working_dir, file_path)
    # For very long results, show only the head and tail
    if len(result) > 200:
        print(f"  Length: {len(result)} characters")
        print(f"  Start: {result[:50]}...")
        print(f"  End: ...{result[-100:]}")
    else:
        print(f"  Result: {result}")
    print("-" * 40)

# 1. Truncation test
test_case("calculator", "lorem.txt")

# 2. Regular file test
test_case("calculator", "main.py")

# 3. Relative path/Subdirectory test
test_case("calculator", "pkg/calculator.py")

# 4. Security boundary test
test_case("calculator", "/bin/cat")

# 5. Missing file test
test_case("calculator", "pkg/does_not_exist.py")
