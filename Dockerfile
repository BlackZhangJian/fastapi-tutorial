# from Images tiangolo/uvicorn-gunicorn-fastapi:python3.7

FROM ccr.ccs.tencentyun.com/drone-test/fastapi-tutorial-base:latest

WORKDIR /fastapi-tutorial

COPY ./requirements.txt /fastapi-tutorial/requirements.txt

RUN /usr/local/bin/python -m pip -r /fastapi-tutorial/requirements.txt

COPY . /fastapi-tutorial

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]