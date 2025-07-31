from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


print("STARTING TESTS")

if __name__ == "__main__":
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

