FROM python:3.11.5


COPY requirements.txt /usr/temp/app/

RUN pip install --no-cache-dir -r /usr/temp/app/requirements.txt

COPY ./app /usr/temp/app/
COPY ./src/ /usr/temp/src/
COPY ./tests /usr/temp/tests/
COPY ./uploads /usr/temp/uploads/

EXPOSE 5000

CMD ["python", "/usr/temp/app/app.py"]
