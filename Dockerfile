FROM deepnox/python-ta-lib:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && \
	echo "0 10 * * * python3 /app/inv_adv.py" > mycron.txt && \
	cat mycron.txt | crontab -
ENTRYPOINT ["tail", "-f", "/dev/null"]
