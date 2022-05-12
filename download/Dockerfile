FROM python:3.7 as download

WORKDIR /app

COPY . .
COPY kaggle.json /root/.kaggle/
RUN pip3 install -r requirements.txt

CMD ["python3", "download.py"] _

