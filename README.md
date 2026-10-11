
# ITC5205 Assessment 2
## AWS-Based YOLOv5 Object Detection System

### Project Overview
This project implements an object detection system using YOLOv5 and AWS cloud services.

### AWS Services
- Amazon EC2 – development and testing
- Amazon S3 – input images and detection results
- AWS Lambda – serverless object detection
- Amazon ECR – Docker image storage
- Amazon API Gateway – HTTP API
- AWS IAM – security and access control
- Amazon CloudWatch – performance monitoring

### System Workflow
1. An image is uploaded to Amazon S3.
2. A signed POST /detect API request specifies the image key.
3. API Gateway invokes AWS Lambda.
4. Lambda uses YOLOv5 to detect objects.
5. The annotated image and JSON results are saved to S3.

### Source Files
- lambda_function.py – Lambda object detection handler
- Dockerfile – Lambda container configuration
- requirements.txt – Python dependencies
- test_api.py – Authenticated API test client

### Model Setup
The deployment uses the upstream Ultralytics YOLOv5
repository and pretrained YOLOv5s model.

The YOLOv5 source and weights are not included in
this repository. Download them separately before
building the container.

### Testing
The system successfully detected four persons and
one bus in the sample image.

Five sequential and five concurrent API requests
returned HTTP status code 200.

### Performance
- Peak Lambda concurrency: 5
- Recorded throttles: 0
- Cold-start initialisation: 7,449.98 ms

### Security
API Gateway uses AWS IAM authorization.
No AWS access keys or credentials are stored
in this repository.
