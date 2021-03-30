FROM python:3.8.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["streamlit", "run", "./person_dashboard.py"]