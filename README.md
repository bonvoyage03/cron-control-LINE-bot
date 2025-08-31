# cron-control-line-bot

A Kubernetes-based LINE Bot to control CronJobs using Google Drive flags. Toggle CronJobs ON/OFF by sending on/off commands via LINE without direct access to the cluster.

## Features

- Turn CronJobs ON/OFF via LINE messages
- Google Drive as a centralized read/write flag store
- Secure service account storage using SealedSecrets
- Lightweight FastAPI + Uvicorn server

## Setup

1. Google Drive
    - Create a cron-flag.txt file with enabled=true/false.
    - Share the file with a Google service account.

2. SealedSecret
    - Store the service account JSON as a SealedSecret.
    - Mount it in the LINE Bot Deployment.

3. LINE Bot
    - Set CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET as environment variables.
    - Deploy using the provided Kubernetes Deployment manifest.

4. CronJob
    - Read the Drive flag file at startup.
    - Exit if enabled=false.

## Usage

Send on or off to the LINE Bot to control your CronJob.
The CronJob will check the Google Drive flag and run only if enabled.

## Dependencies

- Python 3.11
- FastAPI, Uvicorn
- google-api-python-client, google-auth
- line-bot-sdk-python
