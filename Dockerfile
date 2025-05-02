FROM python:3.10.5

RUN mkdir /usr/app
WORKDIR /usr/app

COPY . .

RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3" , "app.py"]