# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

COPY bids_converter.py bids_converter.py
