FROM python:3


ADD source/barcode.py /


RUN pip install pystrich


CMD [ "python", "/barcode.py"]