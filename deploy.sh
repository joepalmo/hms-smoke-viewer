#!/bin/bash
set -e

# Define deployment settings
REGION="us-east1"
PROJECT_ID="proven-dream-439521-t5"
REPO_NAME="smoke-viewer-repo"
SERVICE_NAME="hms-smoke-viewer"
SERVICE_ACCOUNT_EMAIL="web-application@proven-dream-439521-t5.iam.gserviceaccount.com"

# Build Docker image for Cloud Run's architecture
docker buildx build --platform linux/amd64 -t $SERVICE_NAME . --load

# Tag and push to Google Artifact Registry
docker tag $SERVICE_NAME $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --service-account $SERVICE_ACCOUNT_EMAIL
