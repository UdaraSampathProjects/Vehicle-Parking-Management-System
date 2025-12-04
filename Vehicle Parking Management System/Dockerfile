# Use official Python image

FROM python:3.10-slim
 
# Set working directory

WORKDIR /app
 
# Copy files

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
 
COPY app.py .
 
# Expose port and run

EXPOSE 8000

CMD ["python", "app.py"]

 