FROM python:3.9.1-buster
EXPOSE $PORT
ENV ENV prod
WORKDIR /app
RUN pip install gunicorn
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn -w 2 --bind 0.0.0.0:$PORT app:app
