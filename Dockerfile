FROM apache/airflow:3.0.0

# Copy your requirements.txt into the image
COPY requirements.txt /requirements.txt

# Install requirements
RUN pip install --no-cache-dir -r /requirements.txt
