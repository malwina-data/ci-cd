import re
import logging
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ERROR_PATTERN = r"boolean org\.bouncycastle\.asn1\.ASN1TaggedObjectParser\.hasTag\(int, int\)"
EML_PATTERN = r"Got index name \((.*?)\.eml\)"
pattern = ERROR_PATTERN
LOG_FILE_PATH = r"log.txt"
context_length: int = 200

app = Flask(__name__)

def find_context_before_pattern(
        full_path: str, pattern: str = ERROR_PATTERN, context_length: int = 200
) -> [str]:
    """
    Searches for a specific error pattern in the log file and extracts the name
    of the `.eml` file found in the context preceding the error.
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


@app.route('/find_eml', methods=['GET'])
def get_failed_email():
    """
    Endpoint to trigger the log search and return the name of the failed email.
    """
    try:
        # Możesz dostarczyć własną ścieżkę pliku logu przez query params
        log_path = request.args.get('log_file', LOG_FILE_PATH)
        failed_email = find_context_before_pattern(log_path)

        if failed_email:
            return jsonify({"status": "success", "failed_email": f"{failed_email}.eml"}), 200
        else:
            return jsonify({"status": "error", "message": "No error pattern or `.eml` file name found in the logs."}), 404

    except Exception as error:
        return jsonify({"status": "error", "message": str(error)}), 500


if __name__ == "__main__":
    # Uruchomienie aplikacji webowej
    app.run(host='0.0.0.0', port=5000)
