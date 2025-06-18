# 🛡️ Network Security Threat Detection API

This project is an end-to-end Machine Learning pipeline for predicting and analyzing potential threats in network data. It uses **FastAPI** for deploying the model as a RESTful service.

---

## 🚀 Features

- **Model Training**: Train the ML model using clean network traffic data.
- **Prediction Endpoint**: Make real-time predictions on new network data.
- **Modular Architecture**: Clean project structure following industry best practices.
- **MongoDB Integration**: Seamless data storage and retrieval.
- **Logging and Exception Handling**: Centralized and detailed.

---

## 📂 Project Structure

NETWORKSECURITY/
├── data_schema/ # Contains schema info for validating input data

├── final_model/ # Serialized model after training 

├── logs/ # Logs generated during training/inference

├── NetworkData/ # Input data folder

├── networksecurity/ # Core package with modular components

│ ├── components/ # Data ingestion, transformation, model trainer, etc.

│ ├── constants/ # Constants used across the pipeline

│ ├── entity/ # Data entity definitions

│ ├── exception/ # Custom exceptions

│ ├── logging/ # Logging utility

│ ├── pipeline/ # Main training/prediction pipelines

│ └── utils/ # Helper functions

├── notebooks/ # Jupyter notebooks for EDA and testing

├── prediction_output/ # Saved predictions

├── templates/ # HTML templates (if any)

├── valid_data/ # Processed/validated input data

├── app.py # FastAPI app defining routes

├── main.py # For Testing only

├── push_data.py # Utility to push data to MongoDB

├── test_mongodb.py # Script to test MongoDB connection

├── requirements.txt # Python dependencies

├── setup.py # Installation script

├── Dockerfile # Docker configuration

└── README.md # 📄 Project documentation


---

## 🧪 API Endpoints

Once the server is up (`uvicorn main:app --reload`), Swagger UI is available at:

http://localhost:8000/docs


### Routes:

| Method | Endpoint     | Description         |
|--------|--------------|---------------------|
| `GET`  | `/`          | Index Route         |
| `GET`  | `/train`     | Trigger model training |
| `POST` | `/predict`   | Send JSON data and receive prediction |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/networksecurity.git
cd networksecurity

```

### 2.  Create and Activate Conda Environment

```bash
conda create -n netsecenv python=3.9 -y
conda activate netsecenv

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt


```
### 4. Set Environment Variables
Create a .env file with your MongoDB URI:

```bash
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster0.mongodb.net/



``` 
### 5. Run the Server

```bash
uvicorn main:app --reload
