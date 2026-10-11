
FROM public.ecr.aws/lambda/python:3.12

# Install Linux libraries needed for object detection
RUN dnf install -y \
    git \
    libgomp \
    libxcb \
    && dnf clean all

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Copy and install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install --no-cache-dir \
    -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Remove GUI OpenCV and install the headless version
RUN pip uninstall -y opencv-python opencv-contrib-python \
    && pip install --no-cache-dir \
    --force-reinstall --no-deps opencv-python-headless

# Copy YOLOv5 and the trained model
COPY yolov5/ ${LAMBDA_TASK_ROOT}/yolov5/
COPY yolov5s.pt ${LAMBDA_TASK_ROOT}/

# Copy Lambda function
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]
