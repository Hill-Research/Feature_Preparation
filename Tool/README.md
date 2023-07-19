# Data Preparation Tools 
| task  | model |
| ------------- | ------------- |
| tag  | number, tag2  |
| segment  | seg, eng_dict  |
|translate| trans, trans_csv, google, google_csv|
|delete| delete, del_after_seg|
# Import
```
import from data_prep import process
```
Download the data_prep folder,and put it in the same directory level of your working python file.
# API:
```
process(input, task, model)
```
task: tag, segment, translate<br/>
model: number, tag2, seg, seg2, trans, google<br/>
input: '/path/to/files' or 'file_name.txt' or a string to translate(ONLY available for 'translate' task)<br/>
### For example, use 'google' model to translate the en_diagnosis.txt to Chinese
```
import from data_prep import process
process("en_diagnosis.txt", "translate", "google")
```

## tag
part-of-speech (POS) tagging
### number: 中文；值/数量
### tag2: 中文；Diagnosis 
more features upcoming...
## seg
segmentation
### seg: default segmentaion model
### eng_dict: English segmentation with a custom dictionary built from MeSH
## translate 
Chinese to English
### trans: CSNAMT model. Not limited in mainland China
###  trans_csv: CSNAMT model. Input txt file. Save the original text in first column and save translated file in a new column named "trans" in a csv.format
### google: Faster, limited usage in mainland China
### google_csv: Input txt file. Save the original text in first column and save translated file in a new column named "trans" in a csv.format
To be noticed, TGoogle Translate API request was rate-limited.In case of getting Exception 429, it means "Too Many Requests" and you might need to consider  restart the Modem or switch a network to change the IP.
## delete
"rm_dict.txt": The dictionary that contains all the unwanted punctuations. user can specify their own custom dictionary. </br>
"delete" task removes unwanted strings, mainly punctuation, from user-specified input file/directory, using rm.txt as a dictionary.
### delete: 
Default mode mainly for pre-segmented files. 
### del_after_seg: 
SPECIFIC for removing punctuations in segmented files. Will remove the entire line, leaving no empty line.</br>
Example:</br>
|| process("input.txt","delete","delete")  | process("segResult.txt","delete","del_after_seg")|
|----------| ------------- | ------------- |
| before  | cancer; II) Type 2 diabetes, Ischaemic heart disease, Cerebrovascular disease, Deep vein thrombosis"| 生育</br>计划</br>，</br>并</br>采取有效</br>的</br>避孕措施</br> |
| after  | cancer II Type 2 diabetes Ischaemic heart disease Cerebrovascular disease Deep vein thrombosis| 生育</br>计划</br>并</br>采取有效</br>的</br>避孕措施</br> |


