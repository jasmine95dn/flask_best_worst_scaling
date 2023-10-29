
# pull the python image
FROM python:3.6

# copy the entire current working directory into the container
COPY . .

# run requirements installment
RUN pip install -r requirements.txt

# run the application (currently in development mode)
CMD ["python", "main.py"]



