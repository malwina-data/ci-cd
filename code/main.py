
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ERROR_PATTERN = r"boolean org\.bouncycastle\.asn1\.ASN1TaggedObjectParser\.hasTag\(int, int\)"
EML_PATTERN = r"Got index name \((.*?)\.eml\)"
pattern = ERROR_PATTERN
LOG_FILE_PATH = r"log.txt"
context_length: int = 200

def find_context_before_pattern(
        full_path: str, pattern: str = ERROR_PATTERN, context_length: int = 200
) -> [str]:
    """
    Searches for a specific error pattern in the log file and extracts the name
    of the `.eml` file found in the context preceding the error.

    Args:
        full_path (str): Path to the log file.
        pattern (str): Regex pattern to search for the error.
        context_length (int): Number of characters to extract before the matched pattern.

    Returns:
        Optional[str]: Name of the `.eml` file, or None if the pattern or `.eml` file is not found.
    """
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            log_text = file.read()
        logger.info(f"Log in text is open")
        matches = list(re.finditer(pattern, log_text, re.DOTALL))
        logger.info(f"Error is localized in mail")
        last_match = matches[-1]
        start_index = max(0, last_match.start() - context_length)
        context = log_text[start_index:last_match.start()]
        logger.info(f"Context of error is find ")
        eml_match = re.search(EML_PATTERN, context)
        logger.info(f"Email is found")
        return eml_match.group(1)

    except FileNotFoundError:
        raise FileNotFoundError(f"Log file '{full_path}' does not exist.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    """
    Main script: runs the `find_context_before_pattern` function and outputs the result.
    """
    try:
        failed_email = find_context_before_pattern(LOG_FILE_PATH)

        if failed_email:
            print(f" {failed_email}.eml")
        else:
           print("No error pattern or `.eml` file name found in the logs.")
    except Exception as error:
        print(f"Error: {error}")