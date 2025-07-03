FROM bitnami/kafka:3.4.0

USER root
RUN install_packages python3 python3-pip netcat
COPY . /app
WORKDIR /app
RUN chmod +x /app/start-kafka-with-apps.sh
RUN pip3 install kafka-python psycopg2-binary