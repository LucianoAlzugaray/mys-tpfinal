FROM python

RUN mkdir /app
WORKDIR /app

# RUN chown -R 1000:1000 .
#
# USER 1000
#
# COPY --chown=1000:1000 . .
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]