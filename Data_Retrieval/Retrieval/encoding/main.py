import os
import shutil

from Encoder import Encoder

# Define Constant
INPUT_DIR = "sample"
OUTPUT_DIR = "output"


def list_files(dir):
    """
    Get the list of files in the directory
    @param dir: file directory
    @return: a list of files in the directory
    """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    return files


def create_output_dir():
    """
    Create output directory. If old directory exists, then delete it
    @return: None
    """
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


def main():
    create_output_dir()
    input_files = list_files(INPUT_DIR)
    for input_file in input_files:
        # TODO: should iterate over all files
        if "result" not in input_file: continue
        input_path = os.path.join(INPUT_DIR, input_file)
        print("process file ", input_path)
        encoder = Encoder(input_path)
        encoder.encode()
        output_path = os.path.join(OUTPUT_DIR, input_file)
        print("output file: ", output_path)
        encoder.dump(output_path)


if __name__ == "__main__":
    main()
