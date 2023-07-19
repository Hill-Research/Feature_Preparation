import os
import pandas as pd

# translation - CSANMT model
def trans(file):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks
    from modelscope.msdatasets import MsDataset
    pipeline_ins = pipeline(
        Tasks.translation, 'damo/nlp_csanmt_translation_en2zh')
    # /path/to/files
    if os.path.isdir(file):
        if (not os.path.exists('tran_result')):
            os.mkdir('tran_result')
        count = 0
        for file_name in os.listdir(file):
            path = os.path.join(file, file_name)
            input = MsDataset.load(path)
            output = ""
            name = file_name.split("/")[-1].split(".")[0]
            iteration = iter(input)
            while True:
                try:
                    item = next(iteration)["text"]
                    result = pipeline_ins(item.strip())["translation"]
                    output += item + "\n" + result + "\n"
                except StopIteration:
                    break
            with open('tran_result/{}_result.txt'.format(name), 'w+', encoding='utf-8') as f:
                f.write(output.strip())
                count += 1
            # show progress
            print("File {} translated with CSANMT.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if (not os.path.exists('tran_result')):
            os.mkdir('tran_result')
        input = MsDataset.load(file)
        output = ""
        iteration = iter(input)
        file_name = file.split("/")[-1].split(".")[0]
        while True:
            try:
                item = next(iteration)["text"]
                result = pipeline_ins(item.strip())["translation"]
                output += item + "\n" + result + "\n"
            except StopIteration:
                break
        with open('tran_result/{}_result.txt'.format(file_name), 'w+', encoding='utf-8') as f:
            f.write(output.strip())
        # show progress
        print("File {} translated with CSANMT.".format(file_name))
    # SINGLE STRING
    elif type(file) == str:
        string = str(file)
        result = pipeline_ins(input=string)
        # show progress
        print("Input string translated with CSANMT.")
        return result["translation"]
    else:
        print('Invalid file path or type')

# translation - Google Translate model


def trans_google(file):
    from googletrans import Translator
    import time
    # Set up the translator
    translator = Translator(service_urls=['translate.google.com'])
    translator.raise_Exception = True
    # /path/to/files
    if os.path.isdir(file):
        if (not os.path.exists('tran_google_result')):
            os.mkdir('tran_google_result')
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                output = ""
                name = file_name.split("/")[-1].split(".")[0]
                with open(path, 'r', encoding='utf-8') as f:
                    # Read the contents of the input file
                    # text = f.read()
                    for text in f:
                        # Translate the text
                        result = translator.translate(
                            text, src='en', dest='zh-cn')
                        time.sleep(1)
                        output += text + result.text + "\n"
                        # Write the translated text to the output file
                    with open('tran_google_result/{}_result.txt'.format(name), 'w', encoding='utf-8') as g:
                        g.write(output)
                        count += 1
                    # Show progress
                    print("File {} translated with Google Translate.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if (not os.path.exists('tran_google_result')):
            os.mkdir('tran_google_result')
        output = ""
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r', encoding='utf-8') as f:
            # Read the contents of the input file
            # text = f.read()
            for text in f:
                # Translate the text
                result = translator.translate(text, src='en', dest='zh-cn')
                time.sleep(0.5)
                output += text + result.text + "\n"
            # Write the translated text to the output file
            with open('tran_google_result/{}_result.txt'.format(file_name), 'w', encoding='utf-8') as g:
                g.write(output)
            # Show progress
            print("File {} translated with Google Translate.".format(file_name))
    # SINGLE STRING
    elif type(file) == str:
        result = translator.translate(file, src='en', dest='zh-cn')
        time.sleep(0.5)
        # show progress
        print("Input string translated with Google Translate.")
        return result.text
    else:
        print('Invalid file path or type')




# translation - Google Translate model, csv format
def trans_google_csv(file):
    from googletrans import Translator
    import time
    import csv
    import requests
    # Set up the translator
    translator = Translator(service_urls=['translate.google.com'])
    translator.raise_Exception = True
    max_retries = 3
    retry_delay = 1
    exponent_base = 2
    # /path/to/files
    if os.path.isdir(file):
        if (not os.path.exists('tran_google_csvresult')):
            os.mkdir('tran_google_csvresult')
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                name = file_name.split("/")[-1].split(".")[0]
                with open(path, 'r', encoding='utf-8') as f:
                    # Read the contents of the input file
                    # text = f.read()
                    output = []
                    textdata = []
                    for text in f:
                        # Translate the text
                        for i in range(max_retries):
                            try:
                                result = translator.translate(text.strip(), src='en', dest='zh-cn')
                                output.append(result.text)
                                textdata.append(text.strip())
                            except requests.exceptions.HTTPError as e:
                                if e.response.status_code == 429:
                                    # Too many requests, wait and try again
                                    retry_delay = exponent_base ** i
                                    print(f"Too many requests, waiting {retry_delay} seconds before retrying")
                                    time.sleep(retry_delay)
                                else:
                                    raise e
                        # If we get here, all retries failed
                        raise Exception("Failed to translate text after all retries")
                        #result = translator.translate(text.strip(), src='en', dest='zh-cn')
                        #time.sleep(0.5)
                        
                        # Write the translated text to the output file
                    with open('tran_google_csvresult/{}_result.csv'.format(name), 'w', encoding='utf-8', newline='') as g:
                        combined_list = zip(textdata, output)
                        # Create a CSV writer object
                        writer = csv.writer(g)
                        # Write the first list to the first row with an empty title
                        writer.writerow(['', 'trans'])  # Write the header row
                        for row in combined_list:
                            writer.writerow([row[0], row[1]])
                        count += 1
                    # Show progress
                    print("File {} translated with Google Translate.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if (not os.path.exists('tran_google_csvresult')):
            os.mkdir('tran_google_csvresult')
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r', encoding='utf-8') as f:
            # Read the contents of the input file
            # text = f.read()
            output = []
            textdata = []
            for text in f:
                # Translate the text
                result = translator.translate(text.strip(), src='en', dest='zh-cn')
                time.sleep(0.5)
                output.append(result.text)
                textdata.append(text.strip())
            # Write the translated text to the output file
            with open('tran_google_csvresult/{}_result.csv'.format(file_name), 'w', encoding='utf-8', newline='') as g:
                combined_list = zip(textdata, output)
                # Create a CSV writer object
                writer = csv.writer(g)
                # Write the first list to the first row with an empty title
                writer.writerow(['', 'trans'])  # Write the header row
                for row in combined_list:
                    writer.writerow([row[0], row[1]])
            # Show progress
            print("File {} translated with Google Translate.".format(file_name))
    else:
        print('Invalid file path or type')


# translation - CSANMT model
def trans_csv(file):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks
    from modelscope.msdatasets import MsDataset
    import time
    import csv
    pipeline_ins = pipeline(
        Tasks.translation, 'damo/nlp_csanmt_translation_en2zh')
    # /path/to/files
    if os.path.isdir(file):
        if (not os.path.exists('tran_result')):
            os.mkdir('tran_result')
        count = 0
        for file_name in os.listdir(file):
            path = os.path.join(file, file_name)
            input = MsDataset.load(path)
            output = []
            textdata = []
            name = file_name.split("/")[-1].split(".")[0]
            iteration = iter(input)
            while True:
                try:
                    item = next(iteration)["text"]
                    result = pipeline_ins(item.strip())["translation"]
                    output.append(result)
                    textdata.append(item.strip())
                except StopIteration:
                    break
            with open('tran_result/{}_result.csv'.format(name), 'w+', encoding='utf-8', newline='') as f:
                combined_list = zip(textdata, output)
                # Create a CSV writer object
                writer = csv.writer(f)
                # Write the first list to the first row with an empty title
                writer.writerow(['', 'trans'])  # Write the header row
                for row in combined_list:
                    writer.writerow([row[0], row[1]])
                count += 1
            # show progress
            print("File {} translated with CSANMT.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if (not os.path.exists('tran_result')):
            os.mkdir('tran_result')
        input = MsDataset.load(file)
        output = []
        textdata = []
        iteration = iter(input)
        file_name = file.split("/")[-1].split(".")[0]
        while True:
            try:
                item = next(iteration)["text"]
                result = pipeline_ins(item.strip())["translation"]
                output.append(result)
                textdata.append(item.strip())
            except StopIteration:
                break
        with open('tran_result/{}_result.csv'.format(file_name), 'w+', encoding='utf-8', newline='') as f:
            combined_list = zip(textdata, output)
            # Create a CSV writer object
            writer = csv.writer(f)
            # Write the first list to the first row with an empty title
            writer.writerow(['', 'trans'])  # Write the header row
            for row in combined_list:
                writer.writerow([row[0], row[1]])
        # show progress
        print("File {} translated with CSANMT.".format(file_name))
    # SINGLE STRING
    elif type(file) == str:
        string = str(file)
        result = pipeline_ins(input=string)
        # show progress
        print("Input string translated with CSANMT.")
        return result["translation"]
    else:
        print('Invalid file path or type')
