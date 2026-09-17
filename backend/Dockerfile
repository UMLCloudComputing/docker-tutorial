# Start with the python:3.11 base image
FROM python:3.11

# set the working directory for the following commands
WORKDIR /app

# copy requirements.txt file into /app
COPY requirements.txt ./

# run `pip install --no-cache-dir -r requirements.txt` to install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the files from the directory
COPY . .

# make the directory for sqlite
RUN mkdir -p /app/data

# expose the port for FastAPI
EXPOSE 8000

# run the command to start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
