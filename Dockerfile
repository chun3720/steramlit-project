#Base Image to use
FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME



COPY requirements.txt ./

#install all requirements in requirements.txt
RUN pip install -r requirements.txt

#Copy all files in current directory into app directory
COPY . .
#Change Working Directory to app directory

#Run the application on port 8080
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

