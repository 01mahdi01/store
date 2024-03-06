FROM python:3.9


WORKDIR /usr/src/app
RUN groupadd -r clientuser
RUN useradd -r -g clientuser -G clientuser clientuser
RUN chown -R clientuser:clientuser /usr/src/app
RUN chmod 500 /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install -r requirements.txt
USER clientuser
COPY . .

EXPOSE 8000
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
