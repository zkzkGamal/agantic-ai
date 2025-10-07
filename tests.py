from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def main():
    print(get_files_info("calculator" , "."))
    print("--"*20)
    print(get_files_info("calculator" , "pkg"))
    print("--"*20)
    print(get_files_info("calculator" , "../"))
    print("=="*20)
    print(get_file_content("calculator" , "pkg/calculator.py"))
    print("--"*20)
    print(get_file_content("calculator" , "main.py"))
    print("--"*20)
    print(get_file_content("calculator" , "pkg/p.pyy"))
    print("--"*20)
    print(write_file("calculator" , "zkzk/zkzk.txt" , "hello world 222"))
    print("--"*20)
    print(run_python_file("calculator", "main.py"))
    print("--"*20)
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("--"*20)
    print(run_python_file("calculator", "../main.py"))
    print("--"*20)
    print(run_python_file("calculator", "nonexistent.py"))
if __name__ == "__main__":
    main()
