FROM apache/airflow:3.0.2

# Copy your requirements.txt into the image
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
