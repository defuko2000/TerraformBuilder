From python:3.6

ENV PYTHONUNBUFFERED=1

WORKDIR /TerraformBuilder

COPY requirements.txt /TerraformBuilder/

RUN pip install -r requirements.txt

COPY . /TerraformBuilder/

CMD ["python3", "manage.py", "migrate"]

#CMD ["python","manage.py","runserver", "0.0.0.0:8000"]
