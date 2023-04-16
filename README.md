# File Hider

This is a Python script that allows you to hide a file within another file and recover it later. The script is run from the command line and takes in arguments for the input files and output file.

## To hide a file:

```python
~$ python3 file-hider.py -c camouflaged_file -s secret_file -o output_file
```

### Options

    -c, --camouflaged-file: The file to hide the secret file in.
    -s, --secret-file: The file to hide.
    -o, --output-file: The output file.

---

## To recover hidden files:

```python
~$ python3 file-hider.py -r camouflaged_file
```

### Options

    -r, --recover-file: The camouflaged file to recover files from.
    -d, --destination: The destination folder to recover files to. (optional)

---

## Requirements

This script requires Python 3.

## How it Works

When you hide a file within another file, the script will take the contents of the camouflaged file and append the secret file's contents to it. It adds a custom EOF marker to the end of the camouflaged file to mark the end of the camouflaged data and the start of the secret data. It also adds the name of the secret file to the output data to make it easier to recover later. When you recover files, the script will look for the custom EOF marker and extract the data after it. The script can recover multiple files that have been hidden in the same camouflaged file.
