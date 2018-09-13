FROM python:3.6-alpine3.7

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

LABEL com.epam.legion.model.id="edi-test-model" \
      com.epam.legion.model.version="1.2" \
      com.epam.legion.container_type="model"

ENTRYPOINT ["python"]
CMD ["app.py"]