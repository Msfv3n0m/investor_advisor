FROM deepnox/python-ta-lib:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "inv_adv.py"]
