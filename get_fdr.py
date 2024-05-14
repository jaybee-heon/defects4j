from get_coverage import *
import csv


def make_fdr_command(pid, vid, test_signature):
    command = f"defects4j mutation -w checkout/{pid}_{vid} -t {test_signature} -i all_classes/{pid}-{vid}/all_classes"
    return command

if __name__ == "__main__":
    projects = './projects.txt'
    fdr_result = dict()
    with open(projects) as pf:
        for line in pf:
            pid, vid = line.split()
            output_file = f'./{pid}-{vid}_fdr.json'
            fdr_result[pid + "_" + vid] = dict()

            print(f"Doing checkout...")
            print(f"{pid}-{vid}")
            run_command(make_checkout_command(pid, vid))

            print("Compiling...")
            run_command(make_compile_command(pid, vid))

            print(f"Testing...: {pid}-{vid}")
            run_command(make_test_command(pid, vid))

            test_file_path = "./checkout/" + pid + "_" + vid + "/all_tests"
            with open(test_file_path) as tf:
                all_tests = tf.readlines()

            for test in tqdm(all_tests):
                test_method, test_class = test.split('(')
                test_class = test_class[:-2]
                test_signature = test_class+"::"+test_method

                fdr_result[pid+"_"+vid][test_signature] = dict()

                # fault? bug?
                print("Measuring Bug Detection Rate...")
                print(test_signature)
                run_command(make_fdr_command(pid, vid, test_signature))

                analysis_result = './checkout/' + pid + "_" + vid + "/summary.csv"
                with open(analysis_result, newline='') as file:
                    reader = csv.reader(file)
                    next(reader)
                    result = next(reader)
                    mutants_generated = int(result[0])
                    mutants_covered = int(result[1])
                    mutants_killed = int(result[2])
                    mutants_live = int(result[3])
                    fdr_result[pid + "_" + vid][test_signature] = {"mutants-generated": mutants_generated,
                                                                   "mutants-covered": mutants_covered,
                                                                   "mutants-killed": mutants_killed,
                                                                   "mutants-live": mutants_live,
                                                                   "mutation-score": mutants_killed/mutants_generated}

            with open(output_file, 'w') as wf:
                json.dump(fdr_result, wf, indent=4)
