import os
import pickle

if __name__ == "__main__":
    projects = "./projects.txt"

    with open(projects) as pf:
        for line in pf:
            pid, vid = line.split()
            directory_path = f"./relevant_classes/{pid}-{vid}"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            tmp_dir = f"/tmp/{pid}-{vid}f"

            if not os.path.exists(tmp_dir):
                os.system(f"defects4j checkout -p {pid} -v {vid}f -w {tmp_dir}")
            os.system(f"cd {tmp_dir} && defects4j export -p classes.relevant -o relevant_classes.txt")
            target_dir = f"/app/defects4j/relevant_classes/{pid}-{vid}"
            os.system(f"mv {tmp_dir}/relevant_classes.txt {target_dir}/relevant_classes.txt")
            # break