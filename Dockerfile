FROM python:3.13.4-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /hcs_site

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py makemigrations && \
 python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]