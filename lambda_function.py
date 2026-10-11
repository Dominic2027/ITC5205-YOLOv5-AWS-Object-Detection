
import os
import io
import json
import logging

import boto3
import torch
from PIL import Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
BUCKET = os.environ["IMAGE_BUCKET"]

model = torch.hub.load(
    "/var/task/yolov5",
    "custom",
    path="/var/task/yolov5s.pt",
    source="local",
    device="cpu"
)
model.eval()


def lambda_handler(event, context):
    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        key = body.get("key", "")

        if not key.startswith("input/"):
            return respond(400, {
                "error": "Image must be inside input/"
            })

        image_object = s3.get_object(
            Bucket=BUCKET,
            Key=key
        )

        image_bytes = image_object["Body"].read()
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        results = model(image, size=640)

        detections = json.loads(
            results.pandas().xyxy[0].to_json(
                orient="records"
            )
        )

        rendered = Image.fromarray(
            results.render()[0]
        )

        buffer = io.BytesIO()
        rendered.save(buffer, format="JPEG")

        name = os.path.splitext(
            os.path.basename(key)
        )[0]

        output_key = f"output/{name}-detected.jpg"
        result_key = f"results/{name}.json"

        s3.put_object(
            Bucket=BUCKET,
            Key=output_key,
            Body=buffer.getvalue(),
            ContentType="image/jpeg"
        )

        result_data = {
            "source_image": key,
            "detected_image": output_key,
            "objects": detections,
            "total_objects": len(detections)
        }

        s3.put_object(
            Bucket=BUCKET,
            Key=result_key,
            Body=json.dumps(result_data),
            ContentType="application/json"
        )

        logger.info(
            "Detected %s objects",
            len(detections)
        )

        return respond(200, result_data)

    except Exception:
        logger.exception("Detection failed")
        return respond(500, {
            "error": "Image processing failed"
        })


def respond(status, data):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(data)
    }
