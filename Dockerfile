FROM deepnox/python-ta-lib:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
	rm requirements.txt
CMD ["python3", "inv_adv.py"]
