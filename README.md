# Customer Churn Prediction

A full-stack machine learning application that predicts whether a bank customer is likely to churn, built with a **FastAPI** backend serving a trained **Gradient Boosting Classifier**, and a **Streamlit** frontend for user interaction.

## Overview

This project takes customer banking data (credit score, geography, age, balance, tenure, etc.) and predicts churn probability. Several classification models were trained and compared, with the final model selected based on a balance of recall, precision, and overall accuracy — then fine-tuned further through hyperparameter tuning and decision threshold optimization.

## Architecture

```
User → Streamlit Frontend (app.py) → REST API call → FastAPI Backend (main.py) → Gradient Boosting Model (model.pkl) → Prediction + Probability → back to Frontend
```

## Project Structure

```
customer-churn-prediction/
│
├── backend/                  # FastAPI backend
│   ├── Model/
│   │   ├── predict.py
│   │   ├── FeatureEngineering.py
│   │   └── model.pkl
│   ├── Schema/
│   │   ├── UserInput.py
│   │   └── response.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                 # Streamlit frontend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── notebooks/                # Jupyter notebook(s)
│   └── training.ipynb        # EDA + model building combined
│
├── data/                     # dataset(s)
│   └── customer_churn.csv
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Dataset

The dataset was sourced from **Kaggle** (bank customer churn dataset). It contains customer-level attributes used to predict whether a customer will leave the bank.

| Feature | Description |
|---|---|
| CreditScore | Customer's credit score |
| Geography | Customer's country (France, Spain, Germany) |
| Gender | Customer's gender |
| Age | Customer's age |
| Tenure | Years as a bank customer |
| Balance | Account balance |
| NumOfProducts | Number of bank products used |
| HasCrCard | Whether the customer has a credit card |
| IsActiveMember | Whether the customer is an active member |
| EstimatedSalary | Customer's estimated salary |

*https://www.kaggle.com/datasets/divu2001/customer-churn-rate/data*

## Feature Engineering

Beyond the raw features, the following engineered columns were added to improve model performance (see `FeatureEngineering.py` / `training.ipynb`):

- **has_3_plus_products** — flags customers using 3 or more bank products
- **is_high_risk_age** — flags customers aged between 40–60, identified as a higher-risk churn group
- **has_zero_balance** — flags customers with a zero account balance
- **is_germany** — flags customers based in Germany, found to correlate with higher churn

## Model Development

Multiple classification algorithms were trained and evaluated:

- Logistic Regression
- Support Vector Classifier (SVC)
- Decision Tree Classifier
- Random Forest Classifier
- **Gradient Boosting Classifier** *(final model)*

Models were compared on **recall, precision, train accuracy, and test accuracy**, and Gradient Boosting Classifier was selected as the best-performing model overall.

### Handling Class Imbalance

The dataset had an imbalanced target (churn vs. non-churn), so the model was trained using a **sample weighting** strategy to give more importance to the minority (churn) class during training, rather than treating all samples equally.

### Hyperparameter Tuning

The Gradient Boosting Classifier was further tuned, and the best-performing parameter combination was selected for the final model.

## Threshold Optimization

By default, classifiers use a 0.5 probability threshold to decide the predicted class. At that threshold, the model performed as follows:

| Metric | Default Threshold (0.5) |
|---|---|
| Accuracy | 79% |
| Recall | 75% |
| Precision | 46% |
| ROC-AUC | 0.85 |

Recall was high but precision was low, meaning the model flagged many customers as likely to churn who actually wouldn't — too many false positives for a production use case.

To address this, the **precision-recall curve** was used to identify a threshold that maximizes the F1-score (the balance between precision and recall). The optimal threshold was found to be **0.67**, which produced:

| Metric | Tuned Threshold (0.67) |
|---|---|
| Accuracy | 86% |
| Recall | 59% |
| Precision | 66% |
| F1-Score | 0.63 |
| ROC-AUC | 0.85 |

This threshold is used in production (`predict.py`) so that predictions better balance catching real churners against avoiding false alarms.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Pydantic
- **ML:** scikit-learn, pandas, numpy
- **Model serialization:** pickle
- **Containerization:** Docker, Docker Compose

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health_check` | API health check |
| POST | `/predict` | Returns churn prediction + probability |

**Sample request to `/predict`:**
```json
{
  "CreditScore": 650,
  "Geography": "France",
  "Gender": "Male",
  "Age": 45,
  "Balance": 12000,
  "Tenure": 5,
  "NumOfProducts": 2,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 50000
}
```

**Sample response:**
```json
{
  "response": {
    "prediction": 1,
    "probability": 0.71
  }
}
```

## Getting Started

### Option 1: Docker Compose (Recommended)

The easiest way to run the full application is with Docker Compose, which builds and starts both services together.

```bash
docker-compose up --build
```

This will start:
- **Backend** (FastAPI) at `http://localhost:8000`
- **Frontend** (Streamlit) at `http://localhost:8501`

To stop all services:
```bash
docker-compose down
```

### Option 2: Run Services Individually with Docker

**Backend:**
```bash
cd backend
docker build -t churn-backend .
docker run -p 8000:8000 churn-backend
```

**Frontend:**
```bash
cd frontend
docker build -t churn-frontend .
docker run -p 8501:8501 churn-frontend
```

### Option 3: Run Locally (Without Docker)

**Backend:**
```bash
cd backend
python -m venv myenv
myenv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```
API will be available at `http://127.0.0.1:8000`

**Frontend:**
```bash
cd frontend
python -m venv myenv
myenv\Scripts\activate      # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

- Add automated tests for the API and prediction pipeline
- Track model experiments (e.g. with MLflow) for easier comparison across runs
- Replace hardcoded backend URL in the frontend with an environment variable for deployment flexibility
- Deploy containers to a cloud provider (e.g. AWS ECS, GCP Cloud Run, or Railway)
