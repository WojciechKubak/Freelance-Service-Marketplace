#!/bin/bash

DRY_RUN=$1
REPO_NAME=$2
AWS_HOST_USER=$3

REPO_PATH="/home/$AWS_HOST_USER/$REPO_NAME"

echo "Repository path: $REPO_PATH"

cd "$REPO_PATH" || exit

echo "Pulling latest code from repository..."
[ "$DRY_RUN" != "true" ] && git pull origin main

echo "Building Docker images..."
[ "$DRY_RUN" != "true" ] && docker-compose -f docker-compose.yml build

echo "Stopping existing containers..."
[ "$DRY_RUN" != "true" ] && docker-compose -f docker-compose.yml down --remove-orphans

echo "Starting new containers..."
[ "$DRY_RUN" != "true" ] && docker-compose -f docker-compose.yml up -d

echo "Running migrations..."
[ "$DRY_RUN" != "true" ] && docker-compose -f docker-compose.yml exec app python manage.py migrate

echo "Deployment complete."
