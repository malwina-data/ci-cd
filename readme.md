# Log Pattern Search Script

This script is designed to search a log file for a specific error pattern and extract the `.eml` file name found in the context preceding the error. It uses regular expressions to locate the error pattern and retrieve the relevant email name.


## Requirements

- Python 3.x
- `pytest` for testing (optional, if you want to run the tests)

Install `pytest` using:

```bash
pip install pytest
```

## Files

- **main.py**: The main script that performs the search and error extraction.
- **test_main.py**: The test script using `pytest` to verify the functionality of `main.py`.
- **test_log.txt**: A sample log file used for testing (will be created and delete during testing).

## Functionality

### `find_context_before_pattern`

This function searches for an error pattern in a log file and extracts the name of the `.eml` file found in the context preceding the error.

#### Arguments:

- `full_path (str)`: Path to the log file.
- `pattern (str)`: The regex pattern to search for the error (default is `ERROR_PATTERN`).
- `context_length (int)`: Number of characters to extract before the matched pattern (default is 200).

#### Returns:

- **Optional[str]**: The name of the `.eml` file, or `None` if no matching error or `.eml` file is found.

#### Example usage:

```python
failed_email = find_context_before_pattern("log.txt")
if failed_email:
    print(f"{failed_email}.eml")
else:
    print("No error pattern or `.eml` file name found in the logs.")
```

## Testing

### 1. **Write a test log**

The test function `test_write_test_log` creates a sample log file (`test_log.txt`) containing a test log.

### 2. **Search for the pattern**

The function `test_in_find` calls `find_context_before_pattern` and asserts that the correct `.eml` file name is found.

### 3. **Test file not found exception**

The `test_file_not_found` function tests the behavior when the log file doesn't exist, ensuring that the script raises a `FileNotFoundError`.

#### Run the tests with `pytest`:

```bash
pytest test_main.py
```

## Structure in order :

ci-cd-2/
├── terraform/                  
│   ├── main.tf                                 # Terraform to run infrastracture
├── scripts/                    
│   ├── setup_azure_devops.md                  # Readme.md describe steps with installing Agent on VM
├── pipelines/                  
│   ├── azure_piplines_run_on_VM_Agent.yaml    # Pipeline run when all the enviroment is ready on VM 
│   └── azure_pipelines_on_Azure_Agent.yaml    # Pipeline run on Azure Agent with basic checks
├── code/                       
│   ├── deploy.sh                               # Code runnig main.py on the VM
│   ├── log.txt                                 # Example of logs to process
│   ├── main.py
│   ├── test_main.py
├── .gitignore  
└── README.md                  
