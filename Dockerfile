# from Images tiangolo/uvicorn-gunicorn-fastapi:python3.7

FROM ccr.ccs.tencentyun.com/drone-test/fastapi-tutorial-base:latest

WORKDIR /fastapi-tutorial

COPY ./requirements.txt /fastapi-tutorial/requirements.txt

RUN /usr/local/bin/python -m pip config set global.index http://mirrors.tencentyun.com/pypi/simple \
    && /usr/local/bin/python -m pip config set install.trusted-host mirrors.tencentyun.com \
    && /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip -r /fastapi-tutorial/requirements.txt

COPY . /fastapi-tutorial

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]