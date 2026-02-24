from functions.get_files_info import get_files_info

def print_result(res, indent="  "):
    for line in res.split('\n'):
        print(f"{indent}{line}")

print('get_files_info("calculator", "."):')
print("Result for current directory:")
print_result(get_files_info("calculator", "."))
print()

print('get_files_info("calculator", "pkg"):')
print("Result for 'pkg' directory:")
print_result(get_files_info("calculator", "pkg"))
print()

print('get_files_info("calculator", "/bin"):')
print("Result for '/bin' directory:")
print_result(get_files_info("calculator", "/bin"), indent="    ")
print()

print('get_files_info("calculator", "../"):')
print("Result for '../' directory:")
print_result(get_files_info("calculator", "../"), indent="    ")
