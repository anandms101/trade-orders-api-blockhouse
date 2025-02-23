# Trade Orders API

## Overview

**Trade Orders API** is a simple backend service that manages trade orders via REST APIs. The service accepts trade order details (such as symbol, price, quantity, and order type) and stores them in a database. It also includes a WebSocket endpoint for real-time order status updates (optional).

This project demonstrates:
- **Backend Development** with FastAPI
- **Containerization** with Docker
- **Deployment** on an AWS EC2 instance
- **CI/CD** pipeline setup using GitHub Actions

## Features

- **POST /orders:** Submit a new trade order.
- **GET /orders:** Retrieve all submitted orders.
- **WebSocket (/ws):** Receive real-time order status updates (bonus).
- **Automated Testing:** Ensures API correctness.
- **CI/CD Pipeline:** Automated tests, builds, and deployment.

## Project Structure

```
trade-orders-api/
├── db/
│   └── database.py
├── models/
│   └── models.py
├── routers/
│   ├── orders.py
│   └── websocket.py
├── tests/
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions workflow
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── .dockerignore         # Files/directories to exclude in Docker build
└── README.md              # This file
```

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Docker**
- **Git**

### Local Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/anandms101/trade-orders-api-blockhouse.git
   cd trade-orders-api-blockhouse
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application Locally:**

   ```bash
   uvicorn main:app --reload
   ```

4. **Access API Documentation:**

   - Swagger UI: ```http://127.0.0.1:8000/docs```
   - Redoc: ```http://127.0.0.1:8000/redoc```

### Running Tests

Run your tests with:

```bash
pytest
```

## Docker

### Build the Docker Image

From the project root, run:

```bash
docker build -t trade-orders-api .
```

### Run the Docker Container

```bash
docker run -d -p 80:80 trade-orders-api
```

You can now access the API at ```http://127.0.0.1```.

## AWS EC2 Deployment

### Launch an EC2 Instance

- Log in to AWS Console and navigate to EC2.
- Launch a new instance using an Ubuntu Server AMI (e.g., Ubuntu 20.04 LTS).
- Instance Type: Choose a t2.micro (free tier eligible).
- Configure Security Group:
  - SSH (port 22): Allow from your IP.
  - HTTP (port 80): Allow from 0.0.0.0/0.
- Select or Create a Key Pair: Download the .pem file.

### Deploying on EC2

1. **SSH into Your Instance:**

   ```bash
   chmod 400 <key>.pem
   ssh -i <key>.pem ubuntu@<EC2-Public-IP>
   ```

2. **Install Docker:**

   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Clone Your Repository:**

   ```bash
   git clone https://github.com/anandms101/trade-orders-api-blockhouse.git
   cd trade-orders-api
   ```

4. **Build and Run the Docker Container:**

   ```bash
   sudo docker build -t trade-orders-api .
   sudo docker run -d --name trade-orders-api -p 80:80 trade-orders-api
   ```

5. **Verify Deployment:**

   Open a browser and navigate to: ```http://<EC2-Public-IP>```
   - API documentation: ```http://<EC2-Public-IP>/docs```

## CI/CD with GitHub Actions

This project uses GitHub Actions to automate testing, building, and deployment when changes are merged to main.

Workflow File: ```.github/workflows/ci-cd.yml```

### Setting Up GitHub Secrets

Add the following secrets in your GitHub repository's Settings → Secrets and variables → Actions:
- ```EC2_HOST```: Public IP or DNS of your EC2 instance.
- ```EC2_USER```: SSH username (e.g., ubuntu).
- ```EC2_SSH_KEY```: The full content of your private key.

## API Documentation

After deployment, access your API documentation at:
- Swagger UI: ```http://<EC2-Public-IP>/docs```
- Redoc: ```http://<EC2-Public-IP>/redoc```

## Bonus Features

- **WebSocket Endpoint:**  
  The API includes a WebSocket endpoint at /ws for real-time updates. Use a WebSocket client to test the connection.

## License

MIT License

Copyright (c) 2025 ANAND MOHAN SINGH

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgements

- Built with FastAPI
- CI/CD powered by GitHub Actions
- Containerization using Docker
- Deployed on AWS EC2

