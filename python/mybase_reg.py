import os
import re

# file_path = r"C:\Users\ksong\Mybase8.ini"
last_pattern = re.compile(r"LastRenew.DataEx.App=(\d*)")
first_pattern = re.compile(r"FirstUseOn.UserLic.App=(\d*)")


def read_info(_file_path):
    info = ""

    if not os.path.exists(_file_path):
        print("the file path is incorrect.")

    try:
        with open(_file_path, mode='r', encoding="utf-8") as fp:
            line_list = fp.readlines()
    except Exception:
        print('Error of opening file.')
        return info
    info_line = [item for item in line_list if "LastRenew" in item]
    if not info_line:
        print("can't find the needed info line")
        return info
    info = last_pattern.findall(info_line[0])[0]
    print(f"last launch time: {info}")
    if not info:
        print("can't find the needed info time")
        return info
    return info


def wtite_info(_file_path, last_t):
    all_info = ""

    if not last_t:
        print("the last_t is incorrect.")
        return False
    if not os.path.exists(_file_path):
        print("the file path is incorrect.")
        return False

    try:
        with open(_file_path, mode='r', encoding="utf-8") as fp:
            all_info = fp.read()
    except Exception:
        print('Error of opening file.')
        return False
    if not all_info:
        print("empty content in the file.")
        return False

    first_t = first_pattern.findall(all_info)[0]
    print(f"first launch time: {first_t}")

    replaced_info = re.sub(first_t, last_t, all_info, 1)
    # replaced_info = all_info.replace(first_t, last_t, 1)
    # print("replaced str: ", replaced_info)
    if not replaced_info:
        print("error of replacing the time.")
        return False

    try:
        os.system(f'attrib -r -s -h {_file_path}')
        with open(_file_path, 'w+', encoding="utf-8") as fp:
            fp.write(replaced_info)
    except Exception as err:
        print(f"error of writing info. err: {err}")
        return False
    print("replaced the first launch time with last launch time.")
    return True


def main():
    print(f"{'*'*60}\nuse the last launch time to replace the first launch time.")
    file_path = os.path.join(os.path.expanduser('~'), "Mybase8.ini")
    last_t = read_info(file_path)
    wtite_info(file_path, last_t)
    print("*"*60)


if __name__ == '__main__':
    main()
