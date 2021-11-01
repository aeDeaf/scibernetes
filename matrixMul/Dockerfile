FROM python:3
ADD . /app
COPY requirements.txt ./app
RUN pip install -r ./app/requirements.txt
COPY matrixmul_app.py ./app
WORKDIR ./app
EXPOSE 5000
CMD ["python", "matrixmul_app.py"]