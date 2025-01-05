import pytest
import os
from main import find_context_before_pattern

def test_write_test_log():
    test_log = """email for user9@example.org, attachment 'update_report.pdf' ready.
                  Email sent to user9@example.org with subject 'Latest Updates'.
                  Got index name (user9_update.eml).
                  java.lang.NoSuchMethodError: 'boolean org.bouncycastle.asn1.ASN1TaggedObjectParser.hasTag(int, int)'"""
    log_file_path = "test_log.txt"
    with open(log_file_path, "w", encoding="utf-8") as file:
        file.write(test_log)

def test_in_find():
    result = find_context_before_pattern('test_log.txt')
    assert result == "user9_update"
    
def test_file_not_found():
    log_file_path = "non_existent_log.txt"

    with pytest.raises(FileNotFoundError):
        find_context_before_pattern(log_file_path)
        os.remove('test_log.txt')

