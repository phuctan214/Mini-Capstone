FROM python:3.8.12
RUN pip install --upgrade pip
RUN pip install --upgrade cython
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 1010
COPY . /app
ENTRYPOINT ["python"]
CMD ["zipkin_server.py"]