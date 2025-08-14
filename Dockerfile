# runtime image for your app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# only if you need OS packages; keep minimal
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# install Python deps first for better cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code last
COPY . .

# expose only if your app serves HTTP; adjust as needed
# EXPOSE 8080
CMD ["python", "app.py"]
