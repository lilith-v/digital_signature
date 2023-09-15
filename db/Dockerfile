

FROM postgres:14 as pg
RUN mkdir -p /workspace
RUN chmod 777 /workspace
ADD init.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init.sh 








