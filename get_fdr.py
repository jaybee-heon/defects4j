from get_coverage import *


def make_fdr_command(pid, vid, test_signature):
    command = "defects4j mutation -w checkout/"+pid+"_"+vid+" -t "+test_signature
    return command

if __name__ == "__main__":
    projects = './projects.txt'
    fdr_result = dict()
    with open(projects) as pf:
        for line in pf:
            pid, vid = line.split()
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

            for test in all_tests:
                test_method, test_class = test.split('(')
                test_class = test_class[:-2]
                test_signature = test_class+"::"+test_method

                fdr_result[pid+"_"+vid][test_signature] = dict()

                # fault? bug?
                print("Measuring Bug Detection Rate...")
                print(test_signature)
                run_command(make_fdr_command(pid, vid, test_signature))

                fdr_file = './checkout/' + pid + "_" + vid + "/fdr.xml"

                tree = ET.parse(fdr_file)
                root = tree.getroot()

                mutants_generated = root.get('mutants-generated')
                mutants_killed = root.get('mutants-killed')
                mutation_score = root.get('mutation-score')

                fdr_result[pid + "_" + vid][test_signature] = { "mutants-generated": mutants_generated,
                                                                "mutants-killed": mutants_killed,
                                                                "mutation-score": mutation_score }

