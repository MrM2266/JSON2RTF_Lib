FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install python-multipart
COPY app/ .

ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]