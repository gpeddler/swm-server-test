# SWM-SERVER-TEST
[![python](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


> This is sample server created for SWM lecture.


## Dev Settings

### venv

Python 3.12 이상이 필요합니다.

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

### install requirements

```bash
pip install -r requirements.txt
```

테스트와 포매터를 포함한 개발 의존성은 다음과 같이 설치합니다.

```bash
pip install -r requirements-dev.txt
```

### customize env

```
DATABASE_URL=sqlite:///database.db
```

### run

```bash
make dev
```

## Python Settings

- asdf: https://asdf-vm.com/guide/getting-started.html
- asdf-python: https://github.com/asdf-community/asdf-python?tab=readme-ov-file#install
