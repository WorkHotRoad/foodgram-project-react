FROM python:3.8.5
WORKDIR /code
COPY . /code
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]