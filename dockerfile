FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV GOOGLE_API_KEY=AIzaSyB3xjgb0DF84EvKsvKafVFdih9jpaj4jGQ
CMD ["python", "app.py"]