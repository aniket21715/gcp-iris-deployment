# Fully Automated ML API Deployment with CML, Docker, and GKE

This project demonstrates a complete, end-to-end Continuous Deployment (CD) pipeline for a machine learning model. The system automatically builds, containerizes, and deploys an Iris species prediction API to a Google Kubernetes Engine (GKE) cluster whenever code is pushed to the `main` branch.

The pipeline provides direct feedback to the developer by posting the live API endpoint as a comment on the triggering Git commit using **CML (Continuous Machine Learning)**.

[![GCP](https://img.shields.io/badge/GCP-Google_Cloud-4285F4?logo=google-cloud)](https://cloud.google.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)

---

## 🏛️ Architecture

The continuous deployment process follows this architecture:

1.  **Developer** pushes code to the `main` branch of a GitHub repository.
2.  **GitHub Actions** triggers a workflow.
3.  The workflow job **builds a Docker image** containing the FastAPI application and the pre-trained `model.joblib`.
4.  The image is tagged with the Git commit SHA and **pushed to Google Artifact Registry**.
5.  The workflow authenticates with our **Google Kubernetes Engine (GKE) cluster**.
6.  It updates a Kubernetes `Deployment` manifest with the new image tag and applies it, triggering a rolling update.
7.  A Kubernetes `Service` of type `LoadBalancer` exposes the API to the internet.
8.  **CML** generates a report with the live API endpoint and posts it as a comment on the commit.

 <!-- You can create and host your own diagram image -->

---

## 🛠️ Technology Stack

*   **Model Serving:** FastAPI
*   **Containerization:** Docker
*   **Cloud Provider:** Google Cloud Platform (GCP)
*   **Container Orchestration:** Google Kubernetes Engine (GKE)
*   **Container Registry:** Google Artifact Registry
*   **CI/CD Automation:** GitHub Actions
*   **MLOps Tooling:** Continuous Machine Learning (CML)
*   **ML Library:** Scikit-learn

---

## 📂 Project Structure
Use code with caution.
Markdown
.
├── .github/
│ └── workflows/
│ └── cd-pipeline.yml # GitHub Actions CI/CD workflow
├── app/
│ ├── main.py # FastAPI application
│ └── model.joblib # Pre-trained Iris model
├── k8s/
│ └── deployment.yaml # Kubernetes deployment manifest
├── Dockerfile # Docker recipe for the application
├── requirements.txt # Python dependencies
├── train_model.py # Script to train the model (run once)
└── README.md # This file
Generated code
---

## 🚀 Showcasing the Project: Setup and Deployment Guide

Follow these steps to set up the infrastructure and deploy the application.

### Prerequisites

1.  A [Google Cloud Platform (GCP) Account](https://cloud.google.com/) and a new project.
2.  The [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install) installed and initialized.
3.  A [GitHub Repository](https://github.com/new) containing the project code.
4.  [Docker](https://www.docker.com/products/docker-desktop/) installed locally.

### Step 1: Local Setup

First, train the model by running the training script. This will create the `app/model.joblib` file.

```bash
pip install -r requirements.txt
python train_model.py
Use code with caution.
Step 2: Provision GCP Infrastructure
Execute the following gcloud commands in your terminal. Remember to replace <YOUR_PROJECT_ID> with your actual GCP Project ID.
1. Enable Required APIs
 
gcloud services enable \
    container.googleapis.com \
    artifactregistry.googleapis.com \
    iamcredentials.googleapis.com
Use code with caution.
Bash
2. Create GKE Cluster
This creates a small, auto-scaling Kubernetes cluster.
 
gcloud container clusters create-auto iris-cluster \
    --project=<YOUR_PROJECT_ID> \
    --region=us-central1
Use code with caution.
Bash
3. Create Artifact Registry Repository
This is where our Docker images will be stored.
 
gcloud artifacts repositories create iris-api-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for Iris API" \
    --project=<YOUR_PROJECT_ID>
Use code with caution.
Bash
4. Create and Configure a Service Account for GitHub Actions
This service account allows GitHub Actions to securely access your GCP resources.
 
# Create the service account
gcloud iam service-accounts create iris-cd-sa \
    --display-name="Iris CD Service Account" \
    --project=<YOUR_PROJECT_ID>

# Grant permissions to push to Artifact Registry
gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \
    --member="serviceAccount:iris-cd-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# Grant permissions to deploy to GKE
gcloud projects add-iam-policy-binding <YOUR_PROJECT_ID> \
    --member="serviceAccount:iris-cd-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com" \
    --role="roles/container.developer"

# Create and download a JSON key for the service account
gcloud iam service-accounts keys create gcp-credentials.json \
    --iam-account="iris-cd-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com"
Use code with caution.
Bash
Warning: The gcp-credentials.json file contains sensitive keys. Do not commit this file to your repository.
Step 3: Configure GitHub Secrets
Navigate to your GitHub repository > Settings > Secrets and variables > Actions.
Create a new repository secret named GCP_PROJECT_ID and paste your GCP Project ID as the value.
Create another new repository secret named GCP_SA_KEY.
Copy the entire content of the gcp-credentials.json file you just downloaded and paste it into the value field for GCP_SA_KEY.
Step 4: Trigger the Deployment
Commit all the project files and push them to the main branch.
 
git add .
git commit -m "feat: setup complete API and CD pipeline"
git push origin main
Use code with caution.
Bash
This will trigger the GitHub Actions workflow defined in .github/workflows/cd-pipeline.yml. You can monitor its progress in the "Actions" tab of your repository.
✅ Verification and Testing
Once the pipeline succeeds, CML will post a comment on your commit with the public IP address. You can also retrieve it manually.
1. Get GKE Credentials
 
gcloud container clusters get-credentials iris-cluster --region us-central1
Use code with caution.
 
2. Check Deployment Status
 
# Check if the deployment is available
kubectl get deployment iris-api-deployment

# Check if pods are running
kubectl get pods
Use code with caution.
 
3. Get the External IP Address
Wait for a minute or two for the Load Balancer to be provisioned. The EXTERNAL-IP will change from <pending> to an IP address.
Generated bash
kubectl get service iris-api-service
# NAME                 TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)        AGE
# iris-api-service     LoadBalancer   10.84.15.201   34.136.56.230   80:30886/TCP   2m
Use code with caution.
 
4. Test the Live API
Use curl or your browser to interact with the deployed API.
Generated bash
# Replace 34.136.56.230 with your actual EXTERNAL-IP
export EXTERNAL_IP=34.136.56.230

# Test the root endpoint
curl http://$EXTERNAL_IP/

# Test the prediction endpoint
curl -X POST "http://$EXTERNAL_IP/predict" \
-H "Content-Type: application/json" \
-d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'
# Expected Output: {"prediction_code":0,"predicted_species":"setosa"}

