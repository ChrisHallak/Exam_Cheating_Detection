# Exam Cheating Detection System

A real-time **AI-powered computer vision system for online exam proctoring and cheating detection**. The system processes webcam frames to detect suspicious objects, multiple people, face absence, abnormal head poses, and other behavioral indicators.

The detected events are combined into a **cheating risk score** to help identify potentially suspicious exam behavior.

## Features

* 🎥 **Real-time Webcam Capture** — Continuous webcam frame processing
* 👤 **Face Detection** — Detects whether the candidate is present
* 🧭 **Head Pose Estimation** — Estimates yaw, pitch, and roll angles
* 📱 **Object Detection** — Detects potentially prohibited objects such as:

  * Mobile phones
  * Books
  * Papers / notebooks
  * Laptops
  * Tablets
  * Headphones
  * Calculators
* 👥 **Multiple Person Detection** — Detects additional people appearing in the camera frame
* ⚠️ **Cheating Risk Score** — Combines multiple detection signals into a risk assessment
* 📊 **Live Dashboard** — Displays detection results and alerts in real time
* 📝 **Session Logging** — Records detected events with timestamps
* 🔌 **REST API** — Provides endpoints for integrating the detection system with other applications

## System Architecture

The system follows a real-time computer vision pipeline:

```text
Webcam
   │
   ▼
Frame Capture
   │
   ├──────────────► Face Detection
   │
   ├──────────────► Head Pose Estimation
   │
   ├──────────────► Object Detection
   │
   └──────────────► Multiple Person Detection
                    │
                    ▼
             Event Aggregation
                    │
                    ▼
             Cheating Score
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    Live Dashboard       Session Logging
```

## Project Structure

```text
Exam_Cheating_Detection/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore
├── README.md
│
├── services/               # Computer vision and detection services
│   ├── face_detection/
│   ├── head_pose/
│   ├── object_detection/
│   └── ...
│
├── models/                 # AI model files
│
├── utils/                  # Helper functions and utilities
│
└── logs/                   # Detection/session logs
```

> The exact structure may vary depending on the current implementation.

## Technologies

The project is built using Python and modern computer vision / AI technologies.

| Technology | Purpose                                   |
| ---------- | ----------------------------------------- |
| Python     | Core programming language                 |
| OpenCV     | Webcam capture and image processing       |
| YOLO       | Real-time object detection                |
| MediaPipe  | Face landmarks and head pose estimation   |
| FastAPI    | REST API                                  |
| Uvicorn    | ASGI server                               |
| NumPy      | Numerical and image processing operations |

## Prerequisites

Before running the project, make sure you have:

* **Python 3.12.7** or higher
* A working webcam or camera device
* **Git**
* Sufficient hardware resources for real-time AI inference

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ChrisHallak/Exam_Cheating_Detection.git
cd Exam_Cheating_Detection
```

### 2. Create and activate a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file from the provided example:

#### Windows

```bash
copy .env.example .env
```

#### macOS / Linux

```bash
cp .env.example .env
```

Then update `.env` with the required configuration values.

> Never commit your `.env` file to Git. Make sure it is included in `.gitignore`.

## Usage

### Run the application

If the project exposes a FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Run in production mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run directly

If `main.py` contains the application entry point:

```bash
python main.py
```

## API Documentation

When running with FastAPI, interactive API documentation is automatically available at:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

## Detection Logic

The system analyzes multiple signals instead of relying on a single detection.

Potential suspicious events include:

```text
Candidate absent
      │
      ▼
Suspicious Event
      │
      ├── Multiple people detected
      │
      ├── Prohibited object detected
      │
      ├── Abnormal head rotation
      │
      └── Other behavioral anomalies
              │
              ▼
        Risk Score Update
              │
              ▼
       Suspicion Assessment
```

The final risk assessment can be used by the examination platform to flag sessions that require further review.

## Cheating Risk Score

The risk score is calculated by combining multiple detection signals.

Example factors include:

| Detection               |  Example Risk |
| ----------------------- | ------------: |
| Candidate absent        |          High |
| Multiple people         |          High |
| Mobile phone detected   |          High |
| Book / paper detected   |        Medium |
| Excessive head rotation |        Medium |
| Normal face presence    | Low / No risk |

The exact scoring thresholds and weights are configurable according to the examination requirements.

## Privacy

This project is intended for educational and research purposes.

When deploying an exam proctoring system in a real environment, consider:

* User consent
* Data protection requirements
* Secure storage of captured frames
* Retention policies
* Access control
* Transparency regarding automated detection
* Human review of suspicious events

Automated detections should be treated as **indicators for review**, rather than definitive proof of cheating.

## Troubleshooting

### Webcam is not detected

Make sure:

1. Your webcam is connected.
2. No other application is currently using the camera.
3. The application has permission to access the webcam.
4. OpenCV can access the selected camera device.

### Dependencies fail to install

Make sure you are using the recommended Python version and that your virtual environment is activated:

```bash
python --version
```

Then upgrade pip:

```bash
python -m pip install --upgrade pip
```

And reinstall the dependencies:

```bash
pip install -r requirements.txt
```

### API does not start

Check that the required dependencies are installed and that the `main.py` file exposes the expected FastAPI application:

```python
app = FastAPI()
```

Then run:

```bash
uvicorn main:app --reload
```

## Future Improvements

* [ ] Improve head pose estimation robustness
* [ ] Add additional prohibited object classes
* [ ] Improve false-positive handling
* [ ] Add persistent session storage
* [ ] Add authentication and authorization
* [ ] Add a web-based monitoring dashboard
* [ ] Add exam session reports
* [ ] Add configurable detection thresholds
* [ ] Add GPU acceleration
* [ ] Add Docker deployment
* [ ] Add automated testing and CI/CD

## Disclaimer

This project is intended for **educational, research, and demonstration purposes**.

Computer vision models can produce false positives and false negatives. Detection results should therefore be reviewed in context and should not be considered definitive evidence of academic misconduct without appropriate human verification.

## License

This project is available under the terms specified in the repository's license.

## Author

**Chris Hallak**

GitHub:
https://github.com/ChrisHallak
