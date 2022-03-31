# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

COPY bids_converter.py bids_converter.py
COPY entities.txt entities.txt
COPY modalities.txt modalities.txt
COPY bids_templates/ bids_templates/

