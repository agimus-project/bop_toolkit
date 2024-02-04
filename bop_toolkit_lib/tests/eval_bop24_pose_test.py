#!/usr/bin/env python
import subprocess
import os
import re
from tqdm import tqdm

# Define the input directory
INPUT_DIR = "./bop_toolkit_lib/tests/data/"

# Define the output directory
OUTPUT_DIR = "./bop_toolkit_lib/tests/logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define the dataset dictionary
FILE_DICTIONARY = {
    # "icbin": "cnos-fastsammegapose_icbin-test_7c9f443f-b900-41bb-af01-09b8eddfc2c4.csv",
    # "tudl": "cnos-fastsammegapose_tudl-test_1328490c-bf88-46ce-a12c-a5e5a7712220.csv",
    "lmo": "cnos-fastsammegapose_lmo-test_16ab01bd-f020-4194-9750-d42fc7f875d2.csv",
    # "ycbv": "cnos-fastsammegapose_ycbv-test_8fe0af14-16e3-431a-83e7-df00e93828a6.csv",
    # "tless": "cnos-fastsammegapose_tless-test_94e046a0-42af-495f-8a35-11ce8ee6f217.csv",
    # Add more entries as needed
}

EXPECTED_OUTPUT = {
    "lmo": {
        "bop24_mAP_mssd": 0.6057892170013075,
        "bop24_mAP_mspd": 0.6665039715002681,
        "bop24_mAP": 0.6361465942507878,
    },
}

# Loop through each entry in the dictionary and execute the command
for dataset_name, file_name in tqdm(FILE_DICTIONARY.items(), desc="Executing..."):
    output_file_name = f"{OUTPUT_DIR}/eval_bop24_pose_test_{dataset_name}.txt"
    command = [
        "python",
        "scripts/eval_bop24_pose.py",
        "--renderer_type=vispy",
        "--results_path",
        INPUT_DIR,
        "--eval_path",
        INPUT_DIR,
        "--result_filenames",
        file_name,
        "--num_worker",
        "1",
    ]
    with open(output_file_name, "a") as output_file:
        subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT)
print("Script executed successfully.")


# Check scores for each dataset
for dataset_name, _ in tqdm(FILE_DICTIONARY.items(), desc="Verifying..."):
    log_file_path = f"{OUTPUT_DIR}/eval_bop24_pose_test_{dataset_name}.txt"

    # Read the content of the log file
    with open(log_file_path, "r") as log_file:
        last_lines = log_file.readlines()[-7:]

    # Combine the last lines into a single string
    log_content = "".join(last_lines)

    # Extract scores using regular expressions
    scores = {
        key: float(value) for key, value in re.findall(r"- (\S+): (\S+)", log_content)
    }

    # Compare the extracted scores with the expected scores
    for key, expected_value in EXPECTED_OUTPUT[dataset_name].items():
        actual_value = scores.get(key)
        if actual_value is not None:
            if actual_value == expected_value:
                print(f"{dataset_name}: {key} - PASSED")
            else:
                print(
                    f"{dataset_name}: {key} - FAILED. Expected: {expected_value}, Actual: {actual_value}"
                )
        else:
            print(f"{dataset_name}: {key} - NOT FOUND")

print("Verification completed.")
