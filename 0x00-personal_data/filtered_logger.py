import os
import re
import logging
import mysql.connector
from typing import List

# Replacing patterns
def create_extract_pattern(fields, separator):
    return r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)

def create_replace_pattern(redaction):
    return r'\g<field>={}'.format(redaction)

# Existing PII_FIELDS
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    extract_pattern = create_extract_pattern(fields, separator)
    replace_pattern = create_replace_pattern(redaction)
    return re.sub(extract_pattern, replace_pattern, message)

# Existing RedactingFormatter
class RedactingFormatter(logging.Formatter):
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt

# Existing code for get_logger, get_db, main

if __name__ == "__main":
    main()
