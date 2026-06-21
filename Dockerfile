# setting up the base image
FROM python:3.11-slim

# setting up the working directory
WORKDIR /app
# copying the requirements file and installing the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copying the rest of the application code
COPY . .

# exposing the port for the application
EXPOSE 8000

# Running with port mapping + .env file
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Running with volume mapping + .env file

# build the Docker image
# docker build -t humanitarian-report-agent .

# running the Docker container with port mapping and volume mapping
# docker run -p 8000:8000 --env-file .env humanitarian-report-agent

# running with volumne(persistent storage) mapping + .env file
# docker run -p 8000:8000 --env-file .env \
# -v $(pwd)/lang_food_poverty_output:/app/lang_food_poverty_output \
# humanitarian-report-agent
