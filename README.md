# containerized-3-tier-app
Rahti Deployment of Full‑Stack Application

Overview
This project is a simple full‑stack web application deployed on Rahti, CSC’s Kubernetes/OpenShift platform.
It includes:

Frontend (React/Vite)

Backend (Flask or Node.js)

MySQL database with persistent storage (PVC)

Rahti YAML files for deployments and services

System Architecture Diagram

                 ┌──────────────────────────────┐
                 │          Frontend             │
                 │      (React / Vite App)       │
                 └──────────────┬───────────────┘
                                │
                                │ HTTP Requests
                                ▼
                 ┌──────────────────────────────┐
                 │      Backend Service          │
                 │   (Stable ClusterIP / DNS)    │
                 └──────────────┬───────────────┘
                                │
                                │ Load Balancing
                                ▼
        ┌──────────────────────────────────────────────────┐
        │                 Backend Pods (1–3)                │
        │  (Flask / Node.js API, auto‑scaled & self‑healed) │
        └──────────────┬──────────────┬────────────────────┘
                       │              │
                       │              │
                       ▼              ▼
                 ┌──────────────────────────────┐
                 │         MySQL Service         │
                 │   (Internal DB endpoint)      │
                 └──────────────┬───────────────┘
                                │
                                │ DB Connection
                                ▼
                 ┌──────────────────────────────┐
                 │            MySQL Pod          │
                 │   (Reads secrets & uses PVC)  │
                 └──────────────┬───────────────┘
                                │
                                │ Persistent Storage
                                ▼
                 ┌──────────────────────────────┐
                 │        Persistent Volume      │
                 │      (Data survives restarts) │
                 └───────────────────────────────┘


Project Structure

project/
│
├── frontend/                 # React/Vite frontend
├── backend/                  # Backend API (Flask or Node.js)
└── rahti/                    # YAML files for Rahti deployment
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── mysql-deployment.yaml
    ├── mysql-service.yaml
    ├── mysql-pvc.yaml
    └── mysql-secret.yaml     # ignored in Git

1. Building & Publishing Docker Images

Backend
Build the backend image:
docker build -t <dockerhub-username>/backend:v1 .

Push it:
docker push <dockerhub-username>/backend:v1

Frontend
Build the frontend image:
docker build -t <dockerhub-username>/frontend:v1 .

Push it:
docker push <dockerhub-username>/frontend:v1

These image tags are referenced in the Rahti deployment YAML files.

2. Deploying MySQL on Rahti

Step 1: Create the PVC

oc apply -f rahti/mysql-pvc.yaml

Step 2: Create the Secret

oc apply -f rahti/mysql-secret.yaml

Step 3: Deploy MySQL

oc apply -f rahti/mysql-deployment.yaml
oc apply -f rahti/mysql-service.yaml

3. Deploying the Backend

Deploy backend:

oc apply -f rahti/backend-deployment.yaml
oc apply -f rahti/backend-service.yaml

4. Deploying the Frontend

Deploy frontend:

oc apply -f rahti/frontend-deployment.yaml
oc apply -f rahti/frontend-service.yaml

Then create a Route in Rahti to expose the frontend publicly.

You will get a URL like: https://frontend-route-three-tier-app.2.rahtiapp.fi/

5. How Components Communicate

Frontend → Backend
The frontend does not know pod IPs.
It communicates through a Service:

Kubernetes load‑balances requests to all backend pods.

Backend → MySQL
Backend connects using secret values: 

MYSQL_ROOT_PASSWORD
MYSQL_DATABASE

And uses the internal service name: mysql-service

MySQL → PVC
MySQL stores data on the PVC, so data persists even if the pod is deleted.
