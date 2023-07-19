# UKBReader 
This README provides an overview of the data retrieval subprograms used in the UKBiobank dataset. These subprograms are specifically designed to extract feature vectors from the UKBiobank dataset, serving the purpose of facilitating further development and utilization of an AI model for matching similar patients.

## CSV_UKB_Feature_Design_final_version2_6262023.xls
This file is used to extract feature vectors from the UKBiobank dataset. It follows the feature vector design documentation and provides a structured approach to extract the desired features.

## NameGenerator.py 
The NameGenerator.py script is used to generate column names for the data retrieved from the UKBiobank dataset. It utilizes information from different sheets, such as 'basic-profile-834', 'diagnosis-13450', 'treatment-5680', and 'result-512', in the Excel file “CSV_UKB_Feature_Design_final_version2_6262023.xls”.
### Prerequisites
1) Python 3.x
2) xlrd library

### Installation
1) Clone the repository or download the script file.
2) Install the required dependencies using the following command:
```
pip install xlrd
```
### Usage
1) Download the Excel file `CSV_UKB_Feature_Design_final_version2_6262023.xls`, `name.txt` and place the Excel file in the same directory as the name_generator.py script. 
2) Open a Python IDE and provide the name of the Excel file （specify the correct file path as your needs）as a parameter:
```
excel_name = 'CSV_UKB_Feature_Design_final_version2_6262023.xls'
name_generator = NameGenerator(excel_name)
```
4) Run the name generation process by calling the run method:
```
names, indexs = name_generator.run()
print(names)  # 打印生成的名称
print(indexs)  # 打印生成的索引
```
5) The program will print whether the generated names in each section are unique and if the corresponding indexes are available in the UKB indexes.
6) Use the generated `names` and `indexs` as needed for further processing or output.

## UKBReader.py 
UKBReader.py is a script used to extract data from UK Biobank dataset files and save it into separate CSV files based on predefined feature names and indexes.

### Prerequisites 
1) Python 3.x
2) pandas library
3) numpy library
4) tqdm library

### Installation
1) Clone the repository or download the `UKBReader.py` script.
2) Install the required dependencies using the following command:
```
pip install pandas numpy tqdm
```
### Usage
1) Save the code to a Python script file.
2) Ensure that you have a UKB data file named 0-1000.csv, or specify the correct UKB data file path by modifying the ukb_data variable according to your needs.
3) Specify a directory path to save the extracted data. You can set the save_path variable to your desired path.
4) Run the UKBReader by calling the `run` method:
```
reader.run()
```
5) After running the script, it will start extracting the data and save it to the specified directory. A progress bar will show the extraction progress. Once completed, it will print the total time taken.

## name.txt
The name.txt file contains the original column names from the UKBiobank dataset. It is utilized during the ordered data retrieval process, ensuring the extracted data maintains the defined order.

## DataPreprocesser.py 
The DataPreprocesser class provides methods for preprocessing data in a CSV format. It performs various operations on the data, such as handling missing values, generating string or date values, and transforming columns based on their types. The script is designed to be modular and can be adapted for different datasets.
Note: The current version of the script does not specifically handle the UKB database. Future updates may support preprocessing and fine-tuning for different datasets.

## DateProcesser.py
The DateProcesser module provides functionality for time blurring and standardizing time formats.
Note: The current version of the script does not specifically handle the UKB database. Future updates may support preprocessing and fine-tuning for different datasets.

