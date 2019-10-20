FROM tensorflow/tensorflow:2.0.0-py3-jupyter

RUN pip install --upgrade pip

RUN pip install sklearn

RUN pip install pandas

RUN pip install xgboost

RUN pip install seaborn

#RUN pip install -U nltk