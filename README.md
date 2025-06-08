# 👻 Ghost of Default

**Ghost of Default** is a FastAPI-based machine learning web application for predicting credit default risk. It uses a logistic regression model trained on the [UCI Default of Credit Card Clients dataset](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset).
The app provides RESTful API endpoints for creating, reading, updating, and deleting predicted outcomes and actual default records, with all data stored in a PostgreSQL database.

## Core Features

- 🚀 **FastAPI Integration**: High-performance, modern web API framework.
- 🧠 **Predictive Analytics**: Logistic Regression model (via scikit-learn) for credit default risk prediction.
- 🗄️ **Database Management (PostgreSQL)**: Stores client info, predictions, and actual defaults.
- 🔐 **Data Validation with Pydantic**: Ensures incoming request data matches defined schemas (e.g., types and ranges).
- 🔁 **RESTful API Design**: Versioned endpoints (e.g. `/v1/predictions`) for clear, stateless operations.
- ⚙️ **Configurable Environment**: All database and secret settings are managed via environment variables.

These features allow rapid development of new endpoints and safe handling of data, leveraging FastAPI’s automatic docs and validation.

## System Requirements

- 🐍 **Python** 3.8+
- 🛢️ **PostgreSQL** (local or hosted instance)
- 📦 **Python Dependencies** as listed in `requirements.txt`

## Environment Setup

**1. Clone the repository and navigate into it:**

```bash
git clone https://github.com/sxlecquer/ghost-of-default.git
cd ghost-of-default
```

**2. Create a virtual environment:**

```bash
python -m venv .venv
```

**3. Activate the virtual environment:**

- macOS/Linux

| Shell    | Command to activate virtual environment |
|----------|-----------------------------------------|
| bash/zsh | $ source *\<venv>*/bin/activate         |
| fish     | $ source *\<venv>*/bin/activate.fish    |
| csh/tcsh | $ source *\<venv>*/bin/activate.csh     |
| pwsh     | $ *\<venv>*/bin/Activate.ps1            |

- Windows

| Shell      | Command to activate virtual environment |
|------------|-----------------------------------------|
| cmd.exe    | C:\> *\<venv>*\Scripts\activate.bat     |
| PowerShell | PS C:\> *\<venv>*\Scripts\Activate.ps1  |

*\<venv> must be replaced by the path to the directory containing the virtual environment*

**4. Install the required packages:**

```bash
pip install -r requirements.txt
```

**5. Configure environment variables:**

Copy the example file `backend/.env.example` to `backend/.env` and adjust it as needed. The settings point to your PostgreSQL database. If you change the DB credentials, update this file accordingly.

## How to Run Locally

**1. Start your database**

Ensure PostgreSQL is running and that the database (e.g., `credit_default_db`) exists and is accessible with the credentials specified in your `.env` file.

**2. Launch the app**

From the project root directory, run:

```bash
uvicorn backend.app.main:app --reload
```

This starts the FastAPI server on `http://localhost:8000`. The `--reload` flag enables auto-reload on code changes.

**3. Access the API docs**

Open your browser to `http://localhost:8000/docs` to view the Swagger UI - interactive documentation that lists all endpoints, request/response models, and allows for easy testing.

![image](https://github.com/user-attachments/assets/1563f0b0-b886-4897-a5b1-932fd0e01e02)

## API Usage

### `POST /v1/predictions`
Create a new prediction from client data (JSON body).

#### Example request body:
```json
{
  "limit_bal": 100000,
  "sex": "male",
  "education": "university",
  "marriage": "single",
  "age": 19,
  "repay_status_1": -1,
  "repay_status_2": 0,
  "repay_status_3": 1,
  "repay_status_4": 3,
  "repay_status_5": 5,
  "repay_status_6": -1,
  "bill_amount_1": 1500,
  "bill_amount_2": 5377,
  "bill_amount_3": 46548,
  "bill_amount_4": 9476,
  "bill_amount_5": 3547,
  "bill_amount_6": 15667,
  "pay_amount_1": 34675,
  "pay_amount_2": 8748,
  "pay_amount_3": 23567,
  "pay_amount_4": 12469,
  "pay_amount_5": 256,
  "pay_amount_6": 1244
}
```

### `PUT /v1/predictions/{prediction_id}/actuals`
Update a prediction record with the actual observed outcome.

#### Example request body:
```json
{
  "actual_default": false
}
```

Attaching the true default status allows the system to record outcomes for retraining.

## Dataset

We use the **Default of Credit Card Clients Dataset** (also known as the Taiwan Credit Dataset).  
This dataset, originally from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients), contains:

- 📊 **30,000** client records  
- 🧾 **23 features** including demographic data, credit limits, payment history, bill amounts, and repayment status

The target variable indicates whether the client defaulted on the following month’s payment.
The original CSV file (`default_credit_card.csv`) is included in the `backend` folder for model training and experimentation.

## Retraining

To keep the model up to date, retraining combines the original dataset with newly collected outcomes stored in the database.
Each time actual default outcomes become available, they are appended to the training data, and the logistic regression model is re-fitted on this combined dataset.
This approach allows the model to adapt to changing patterns in user behavior and maintain high predictive performance over time.

Retraining can be triggered by a `backend/ml/model_workflow.py` script that reads the original `default_credit_card.csv` file along with the latest records from the PostgreSQL database, fits a new pipeline, and saves the updated model.

```python
if __name__ == "__main__":
    train_model()  # comment this line
    # retrain_model()  # uncomment to update model with new actual outcomes
```
