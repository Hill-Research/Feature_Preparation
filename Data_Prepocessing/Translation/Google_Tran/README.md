## How to build?
Install GoogleTrans library:
```bash
pip install googletrans==4.0.0-rc1
```
Install xlrd
```bash
pip install xlrd
```

## How to run?
- Place the Excel files (ending with .xls or xlsx) in a directory, say `input` directory
- Run the command
```bash
python main.py input
```
And the tool will translate the first column in each Excel file (assuming it has english words) into Chinese, and attach them to the last column. The translated files will be placed in a drectory named `input_translate`.
