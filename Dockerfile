FROM python:3.7 as requirements

WORKDIR /projet

COPY requirements.txt .
# RUN apk update && apk add python3-dev \
#                         gcc \
#                         libc-dev


# RUN pip install --upgrade pip 
RUN pip3 install -r requirements.txt

