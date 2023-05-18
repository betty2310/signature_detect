### Prerequisites

+ Python > 3.10

### Setup
1. Create a new virtual environment by running the following command:
    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment.
    ```bash
    source venv/bin/activate
    ```
3. Install the required dependencies 
    ```bash
    pip install -r requirements.txt
    ```

### Usage
Run command:
```bash
python signature_extractor.py test.jpg
```
This will create 3 images:
+ `pre_version.jpg`: the image after preprocessing
+ `output.jpg`: the image after extracting signature
+ `croppped_image.jpg`: the image after cropping the signature

| Original image | Preprocessed image | Extracted signature | Cropped signature |
| --- | --- | --- | --- |
| ![Original image](./inputs/img/test.jpg) | ![Preprocessed image](./pre_version.png) | ![Extracted signature](./output.png) | ![Cropped signature](./cropped_image.png) |
