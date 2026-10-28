FROM python:3.13-slim

WORKDIR /prober

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY prober.py .

CMD ["python", "-u", "prober.py"]