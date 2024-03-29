FROM python:3.9

COPY bids_converter.py /app/bids_converter.py
COPY bidsconv_parseargs.py /app/bidsconv_parseargs.py
COPY bidsconv_functions.py /app/bidsconv_functions.py

COPY entities.txt /app/entities.txt
COPY modalities.txt /app/modalities.txt
COPY bids_templates/ /app/bids_templates/