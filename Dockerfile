FROM python:3.9
  
WORKDIR /app

COPY ./ ./
 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]