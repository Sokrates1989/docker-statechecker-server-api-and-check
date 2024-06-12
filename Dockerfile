# PYTHON.
FROM python:3.9

# Enable Virtual Environment.
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip, install and upgrade pip dependencies.
COPY install/pip_install.txt install/pip_upgrade.txt /code/
WORKDIR /code
RUN python3 -m venv $VIRTUAL_ENV \
    && python -m pip install --upgrade pip \
    && pip install --upgrade pip \
    && pip install -r pip_install.txt \
    && pip install -r pip_upgrade.txt --upgrade \
    && rm -rf /root/.cache/pip


### Environment variables ###

## Default settings ##
# Fix print commands not being written to docker logs.
ENV PYTHONUNBUFFERED=1
# Timezone.
ENV TIMEZONE=""

## Statechecker Settings ##
ENV STATECHECKER_SERVER_CONFIG=""

# Google Drive.
ENV GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_FILE="/run/secrets/SET THIS ENVIRONMENT VAR IN SWARM DEPLOY ENVIRONMENTS"

# Database connection.
ENV DB_HOST=""
ENV DB_USER=""
ENV DB_PW=""
ENV DB_PW_FILE=""
ENV DB_NAME=""

# Check Frequency.
ENV CHECK_WEBSITES_EVERY_X_MINUTES="30"
ENV CHECK_GOOGLEDRIVE_EVERY_X_MINUTES="60"

## Messaging ##
ENV STATUS_MESSAGES_TIME_OFFSET_PERCENTAGE="2.5"

# Email.
ENV EMAIL_ENABLED="false"
# Message Frequency.
ENV EMAIL_STATUS_MESSAGES_EVERY_X_MINUTES="60"
# Sender.
ENV EMAIL_SENDER_USER="some.mail@domain.com"
ENV EMAIL_SENDER_PASSWORD_FILE=""
ENV EMAIL_SENDER_PASSWORD=""
ENV EMAIL_SENDER_HOST="smtp.example.com"
ENV EMAIL_SENDER_PORT="587"
# Recipients.
ENV EMAIL_RECIPIENTS_ERROR="mail1@domain.com, mail2@domain.com"
ENV EMAIL_RECIPIENTS_INFORMATION="mail1@domain.com, mail2@domain.com"

# Telegram.
ENV TELEGRAM_ENABLED="false"
# Message Frequency.
ENV TELEGRAM_STATUS_MESSAGES_EVERY_X_MINUTES="60"
# Sender Telegram bot token.
ENV TELEGRAM_SENDER_BOT_TOKEN_FILE=""
ENV TELEGRAM_SENDER_BOT_TOKEN=""
# Recipients.
ENV TELEGRAM_RECIPIENTS_ERROR_CHAT_IDS=""
ENV TELEGRAM_RECIPIENTS_INFO_CHAT_IDS=""

# Copy the app.
COPY . /code
