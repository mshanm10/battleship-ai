FROM python:3.7.4

RUN pip install --upgrade pip

RUN pip install pandas

RUN pip install -U nltk

RUN pip install jupyter

RUN pip install sklearn
