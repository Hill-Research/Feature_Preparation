import os
# deletion - default, remove all the string in the "rm_dict.txt" from the input file/directory
def dele(file): 
    # Load the "rm_dict.txt" as deletion dictionary
    with open('rm_dict.txt') as dict_file:
        dict_list = dict_file.read().splitlines()
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('delete_result')):
            os.mkdir('delete_result')
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                name = file_name.split("/")[-1].split(".")[0]
                with open(path, 'r', encoding='utf-8') as f:
                    # Read the contents of the input file
                    text = f.read()
                    for string in dict_list:
                    # Remove each string from the content
                        text = text.replace(string, ' ')
                        # Write the output text after removal
                    with open('delete_result/{}_result.txt'.format(name), 'w', encoding='utf-8') as g:
                        g.write(text)
                        count += 1
                    # Show progress
                    print("File {} performed removal.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('delete_result')):
            os.mkdir('delete_result')
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r', encoding='utf-8') as f:
            # Read the contents of the input file
            text = f.read()
            for string in dict_list:
                # Remove each string from the content
                text = text.replace(string, ' ')
            # Write the translated text to the output file
            with open('delete_result/{}_result.txt'.format(file_name), 'w', encoding='utf-8') as g:
                g.write(text)
            # Show progress
            print("File {} performed removal.".format(file_name))
    else:
        print('Invalid file path or type')

# deletion 2 - specifically for after-segmented files
def dele2(file): 
    # Load the "rm_dict.txt" as deletion dictionary
    with open('rm_dict.txt') as dict_file:
        dict_list = dict_file.read().splitlines()
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('delete_result')):
            os.mkdir('delete_result')
        count = 0
        for file_name in os.listdir(file):
            if file_name.endswith('.txt'):
                path = os.path.join(file, file_name)
                name = file_name.split("/")[-1].split(".")[0]
                with open(path, 'r', encoding='utf-8') as f:
                    # Read the contents of the input file
                    text = f.readlines()
                    for string in dict_list:
                    # Remove the whole line from the content
                        text = [line for line in text if not any(string in line for string in dict_list)]
                        # Write the output text after removal
                    with open('delete_result/{}_result.txt'.format(name), 'w', encoding='utf-8') as g:
                        g.writelines(text)
                        count += 1
                    # Show progress
                    print("File {} performed removal.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('delete_result')):
            os.mkdir('delete_result')
        file_name = file.split("/")[-1].split(".")[0]
        with open(file, 'r', encoding='utf-8') as f:
            # Read the contents of the input file
            text = f.readlines()
            for string in dict_list:
                # Remove the whole line from the content
                text = [line for line in text if not any(string in line for string in dict_list)]
            # Write the translated text to the output file
            with open('delete_result/{}_result.txt'.format(file_name), 'w', encoding='utf-8') as g:
                g.writelines(text)
            # Show progress
            print("File {} performed removal.".format(file_name))
    else:
        print('Invalid file path or type')