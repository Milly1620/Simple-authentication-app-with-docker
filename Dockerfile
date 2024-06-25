FROM python:3.8

WORKDIR /code

COPY requirements.txt .
COPY . /code

RUN pip install --no-cache-dir -r requirements.txt
          
RUN prisma generate 
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
