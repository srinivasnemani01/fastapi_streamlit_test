FROM tiangolo/uvicorn-gunicorn:python3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /code
COPY config.ini /code
ENTRYPOINT ["python","/code/api_manager.py"]

