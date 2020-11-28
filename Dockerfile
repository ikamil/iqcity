FROM puckel/docker-airflow

ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG DEST_INSTALL=/tmp/install

ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

RUN env

USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg2 sudo wget
# Install chrome headless
RUN (wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -) && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst libpq-dev  && \
    rm -rf /var/lib/apt/lists/*

# Add sudo privileges to airflow user and allow to sudo without password
RUN usermod -aG sudo airflow && \
    sed -i 's/%sudo	ALL=(ALL:ALL) ALL/%sudo	ALL=(ALL:ALL) NOPASSWD:ALL/' /etc/sudoers

# Install require Python dependencies
COPY requirements.dev.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --requirement /tmp/requirements.dev.txt

RUN mkdir -p ${DEST_INSTALL}

ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"

# Make sure Airflow is owned by airflow user
RUN chown -R airflow: ${AIRFLOW_USER_HOME}

USER airflow
