import os
import pickle

if __name__ == "__main__":
    with open("newest.pkl", "rb") as f:
        data = pickle.load(f)
        print(data)

    for pid, vid in data.items():
        if not os.path.exists(f"./relevant_classes/{pid}-{vid}"):
            os.system(f"mkdir ./relevant_classes/{pid}-{vid}")
        tmp_dir = f"/tmp/{pid}-{vid}f"

        if not os.path.exists(tmp_dir):
            os.system(f"defects4j checkout -p {pid} -v {vid}f -w {tmp_dir}")
        os.system(f"cd {tmp_dir} && defects4j export -p classes.relevant -o relevant_classes")
        os.system(f"mv {tmp_dir}/relevant_classes ./relevant_classes/{pid}-{vid}/relevant_classes")
        # break