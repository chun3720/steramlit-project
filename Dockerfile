#Base Image to use
FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


#install all requirements in requirements.txt
RUN pip install -r requirements.txt


#Run the application on port 8080
CMD exec streamlit --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
