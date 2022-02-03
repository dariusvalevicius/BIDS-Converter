# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY bids_converter.py bids_converter.py

