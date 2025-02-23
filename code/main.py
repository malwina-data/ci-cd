import re
import logging
from flask import Flask, jsonify


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ERROR_PATTERN = r"boolean org\.bouncycastle\.asn1\.ASN1TaggedObjectParser\.hasTag\(int, int\)"
EML_PATTERN = r"Got index name \((.*?)\.eml\)"
pattern = ERROR_PATTERN
LOG_FILE_PATH = r"log_1.txt"
context_length: int = 200


app = Flask(__name__)

def find_context_before_pattern(
        full_path: str, pattern: str = ERROR_PATTERN, context_length: int = 200
) -> [str]:
    """
    Szuka określonego wzorca błędu w pliku logu i wyodrębnia nazwę pliku `.eml`,
    który znajduje się w kontekście przed błędem.

    Args:
        full_path (str): Ścieżka do pliku logu.
        pattern (str): Wzorzec regex do wyszukiwania błędu.
        context_length (int): Liczba znaków do wyodrębnienia przed dopasowanym wzorcem.

    Returns:
        Optional[str]: Nazwa pliku `.eml`, lub None, jeśli wzorzec lub plik `.eml` nie zostały znalezione.
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

@app.route('/', methods=['GET'])
def find_email():
    try:
        failed_email = find_context_before_pattern(LOG_FILE_PATH)
        if failed_email:
            return jsonify({"email": f"{failed_email}.eml"})
        else:
            return jsonify({"error": "No error pattern or `.eml` file name found in the logs."}), 404
    except Exception as error:
        logger.error(f"Error in find_email route: {str(error)}")
        return jsonify({"error": str(error)}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
