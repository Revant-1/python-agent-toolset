from functions.write_file import write_file

def test_case(working_dir, file_path, content):
    print(f'write_file("{working_dir}", "{file_path}", "{content[:30]}...")')
    result = write_file(working_dir, file_path, content)
    print(f"  Result: {result}")
    print("-" * 40)

# 1. Overwrite existing file
test_case("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

# 2. Write to a new subdirectory
test_case("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

# 3. Security boundary test
test_case("calculator", "/tmp/temp.txt", "this should not be allowed")
