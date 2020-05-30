FROM python:3.8.2-slim

WORKDIR /usr/app

ARG PIP_LIBRARIES
ENV JUPYTER_TOKEN ""

RUN pip install notebook
RUN pip install $PIP_LIBRARIES

CMD jupyter-notebook --NotebookApp.token=$JUPYTER_TOKEN --ip=0.0.0.0 --port=8888 --allow-root
