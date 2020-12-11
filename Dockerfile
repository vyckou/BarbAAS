FROM python:3.7

ENV TZ=Europe/Vilnius

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY *.py /app/

ENTRYPOINT [ "python", "-u" ,"main.py" ]
