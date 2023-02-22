FROM python:3.10.7-slim-buster 
RUN mkdir -p /home/app
WORKDIR /home/app

RUN python -m pip install --upgrade pip
COPY requirements.txt /home/app/
RUN ls
RUN pip install -r requirements.txt
RUN pip install flask psycopg2-binary plotly dash pandas gunicorn
COPY . /home/app/
CMD python app.py