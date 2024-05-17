from get_coverage import *
import os

def make_relevant_classes_command(pid, vid):
    command = f"defects4j export -p classes.relevant -w checkout/{pid}_{vid} -o ./relevant_classes/{pid}_{vid}/relevant_classes.txt"
    return command

def create_directory_and_file(directory_path, file_name, file_content=""):
    # 디렉토리가 존재하지 않으면 디렉토리를 생성합니다.
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory {directory_path} created.")
    else:
        print(f"Directory {directory_path} already exists.")

    # 파일의 전체 경로를 생성합니다.
    file_path = os.path.join(directory_path, file_name)

    # 파일을 생성하고 내용을 작성합니다.
    with open(file_path, 'w') as file:
        file.write(file_content)
        print(f"File {file_name} created in {directory_path}.")


if __name__ == "__main__":
    projects = "./projects.txt"
    with open(projects) as pf:
        for line in pf:
            pid, vid = line.split()

            print(f"Doing checkout...")
            print(f"{pid}-{vid}")
            run_command(make_checkout_command(pid, vid))

            print("Export...")
            create_directory_and_file(f"./relevant-classes/{pid}_{vid}", "relevant_classes.txt")
            run_command(make_relevant_classes_command(pid, vid))