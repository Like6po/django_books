FROM python:3.10

RUN pip install --upgrade pip
WORKDIR /books_site
COPY requirements.txt /books_site
RUN pip install -r requirements.txt
COPY . .