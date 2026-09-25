from functions.get_files_info import get_files_info

def test() -> None:
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    for item in result:
        print(item)

    print("Result for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    for item in result:
            print(item)

    print("Result for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)

    print("Result for '../' directory:")
    result = get_files_info("calculator", "../")
    print(result)

if __name__ == "__main__":
    test()
