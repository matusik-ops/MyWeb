FROM python:3.10.12
WORKDIR /code
COPY ./MyWeb /code
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python3", "app.py"]