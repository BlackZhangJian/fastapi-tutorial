# from Images tiangolo/uvicorn-gunicorn-fastapi:python3.7

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /fastapi-tutorial

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com

COPY . /fastapi-tutorial

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]