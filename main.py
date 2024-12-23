from flask import Flask, request, jsonify
import numpy as np
import json
import boto3
import re

app = Flask(__name__)

# Configure AWS credentials (replace with your actual credentials)
AWS_ACCESS_KEY_ID = "AKIAXWMA6DHLMPZP6R3D"  # Replace with your actual Access Key ID
AWS_SECRET_ACCESS_KEY = "oiLj+JJH26Jh4YvqgDy7k4ZNnqOEgWhZYJaAjOSG"  # Replace with your actual Secret Access Key
AWS_REGION = "us-east-1"  # e.g., 'us-east-1'


def process_image(image_stream):
    """
    Processes an image of an Egyptian car plate using Amazon Rekognition
    and extracts the two lines of text after removing "Egypt", "مصر", and
    any lines that don't contain Arabic letters or digits.

    Args:
        image_stream: The image stream to process.

    Returns:
        A JSON string in the format: {"lines": ["line1", "line2"]}
    """
    try:
        # Convert image stream to bytes
        image_content = image_stream.read()

        # Create a Rekognition client
        rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        # Call Rekognition to detect text
        response = rekognition_client.detect_text(Image={'Bytes': image_content})

        # Extract detected lines and filter
        lines = []
        for text in response['TextDetections']:
            if text['Type'] == 'LINE':
                line = text['DetectedText']
                line = line.replace("Egypt", "").replace("مصر", "")  # Remove unwanted words

                # Filter to keep only Arabic numbers, letters, and spaces
                arabic_chars = "".join(re.findall(r'[\u0621-\u064A\u0660-\u0669 ]', line))
                print(arabic_chars)
                if arabic_chars.__len__() > 0:
                    lines.append(" ".join(arabic_chars.replace(" ", "")))

        # Ensure only two lines are returned
        if len(lines) > 2:
            lines = lines[:2]  # Keep only the first two lines
        elif len(lines) < 2:
            lines += [""] * (2 - len(lines))  # Add empty strings if needed

        # Format the output
        response = {
            "plateParts": lines
        }
        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})


@app.route('/plate', methods=['POST'])
def plate_recognition():
    """
    Endpoint for car plate recognition.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        response = process_image(image_file.stream)
        return jsonify(json.loads(response))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000, debug=True)
