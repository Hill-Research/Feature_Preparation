import os

# tagging - MAOE model - 值/数量
def tag1(file):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks
    from modelscope.msdatasets import MsDataset
    from adaseq import pipelines
    # load MAOE 
    pipeline_ins = pipeline(
    Tasks.named_entity_recognition, 'damo/nlp_maoe_named-entity-recognition_chinese-base-general')
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('tag_result')):
            os.mkdir('tag_result')
        count = 0
        for file_name in os.listdir(file):
            path = os.path.join(file, file_name)
            input = MsDataset.load(path)
            output = ""
            iteration = iter(input)
            name = file_name.split("/")[-1].split(".")[0]
            while True:
                try:
                    item = next(iteration)["text"]
                    tag_list = pipeline_ins(item.strip())["output"]
                    for tag in tag_list:
                        if (tag['type'] == '值/数量'):
                            output += tag['span'] + "\t" + tag['type'] + "\n"
                except StopIteration:
                    break
            with open('tag_result/{}_result.txt'.format(name), 'w+', encoding = 'utf-8') as f:
                f.write(output.strip())
                count +=1
                # show progress
            print("File {} tagged with MAOE.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('tag_result')):
            os.mkdir('tag_result')
        input = MsDataset.load(file)
        file_name = file.split("/")[-1].split(".")[0]
        output = ""
        iteration = iter(input)
        while True:
            try:
                item = next(iteration)["text"]
                tag_list = pipeline_ins(item.strip())["output"]
                for tag in tag_list:
                    if (tag['type'] == '值/数量'):
                        output += tag['span'] + "\t" + tag['type'] + "\n"
            except StopIteration:
                break
        with open('tag_result/{}_result.txt'.format(file_name), 'w+', encoding = 'utf-8') as f:
            f.write(output.strip())
        # show progress
        print("File {} tagged with MAOE".format(file_name))
    else:
        print('Invalid file path or type')


# tagging - NestedNer model - Diagnosis
def tag2(file):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks
    from modelscope.msdatasets import MsDataset
    # load NestedNer
    pipeline_ins = pipeline(
    Tasks.named_entity_recognition, 'damo/nlp_nested-ner_named-entity-recognition_chinese-base-med')
    # /path/to/files
    if os.path.isdir(file):
        if(not os.path.exists('tag_result')):
            os.mkdir('tag_result')
        count = 0
        for file_name in os.listdir(file):
            path = os.path.join(file, file_name)
            input = MsDataset.load(path)
            output = ""
            iteration = iter(input)
            name = file_name.split("/")[-1].split(".")[0]
            while True:
                try:
                    item = next(iteration)["text"]
                    tag_list = pipeline_ins(item.strip())["output"]
                    for tag in tag_list:
                        output += tag['span'] + "\t" + tag['type'] + "\n"
                except StopIteration:
                    break
            with open('tag_result/{}_result.txt'.format(name), 'w+', encoding = 'utf-8') as f:
                f.write(output.strip())
                count +=1
            # show progress
            print("File {} tagged with NestedNer.".format(file_name))
    # SINGLE FILE NAME
    elif os.path.isfile(file) and file.endswith('.txt'):
        if(not os.path.exists('tag_result')):
            os.mkdir('tag_result')
        input = MsDataset.load(file)
        file_name = file.split("/")[-1].split(".")[0]
        output = ""
        iteration = iter(input)
        while True:
            try:
                item = next(iteration)["text"]
                tag_list = pipeline_ins(item.strip())["output"]
                for tag in tag_list:
                    output += tag['span'] + "\t" + tag['type'] + "\n"
            except StopIteration:
                break
        with open('tag_result/{}_result.txt'.format(file_name), 'w+', encoding = 'utf-8') as f:
            f.write(output.strip())
        # show progress
        print("File {} tagged with NestedNER".format(file_name))
    else:
        print('Invalid file path or type')
