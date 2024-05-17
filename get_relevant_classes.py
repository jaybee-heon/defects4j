from get_coverage import *

def make_relevant_classes_command(pid, vid):
    command = f"defects4j export -p classes.relevant -w checkout/{pid}_{vid}"
    return command

if __name__ == "__main__":
    projects = "./projects.txt"
    with open(projects) as pf:
        for line in pf:
            pid, vid = line.split()
            
            print(f"Doing checkout...")
            print(f"{pid}-{vid}")
            run_command(make_checkout_command(pid, vid))

            print("Export...")
            run_command(make_relevant_classes_command(pid, vid))