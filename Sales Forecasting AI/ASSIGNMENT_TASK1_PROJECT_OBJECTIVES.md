# Assignment Task 1: Project Objectives — Sales Forecasting AI

**Learner context:** Internship at a small independent software development company exploring AI solutions for clients.

**Area of AI selected:** **Predictive analytics / time-series forecasting** — a sales and demand forecasting system.

**Project name:** Sales Forecasting AI

**Date:** June 2026

---

## 1. Vocational scenario

The company owner wants to diversify into AI after reading Assignment 1. This project demonstrates one practical AI capability: **forecasting future monthly sales revenue and product quantity** from historical retail transaction data, delivered through a Python forecasting engine and a web-based chatbot interface for non-technical users.

This aligns with a common client need: small businesses that want data-driven planning without hiring a dedicated analytics team.

---

## 2. Summary of overall purpose

The **Sales Forecasting AI** project will:

1. **Ingest** historical store sales transactions from a structured CSV dataset.
2. **Prepare** clean monthly time-series data suitable for machine learning.
3. **Train** a time-series forecasting model on past sales and quantity patterns (including trend and seasonality).
4. **Predict** future monthly sales and quantity for a user-defined horizon (e.g. 3, 12, or 24 months).
5. **Present** results through exportable CSV files, charts, summary statistics, and a conversational chatbot UI so the company can demonstrate the solution to potential clients.

The solution supports the owner’s goal of proving the company can build **functional, client-facing AI products** in the business intelligence domain.

---

## 3. Project objectives

| ID | Objective | Description |
|----|-----------|-------------|
| O1 | Data readiness | Identify a suitable data source, clean it, and split it into training, validation, and testing datasets. |
| O2 | Accurate forecasting | Produce monthly forecasts for **Sales** and **Quantity** that are sufficiently accurate for planning purposes. |
| O3 | Seasonality handling | Model recurring yearly patterns (e.g. peak months) in retail demand. |
| O4 | Usable outputs | Generate `forecast_results.csv` and visual charts that stakeholders can interpret. |
| O5 | Interactive demonstration | Provide a chatbot UI so users can request forecasts, charts, comparisons, and statistics in natural language. |
| O6 | Evaluability | Measure forecast quality on held-out test data using standard error metrics. |
| O7 | Deployability | Run locally via FastAPI so the company can demo the product on a laptop without cloud costs. |

---

## 4. Success criteria and functional requirements

Success criteria define **how** each objective will be judged. Functional requirements describe **what the system must do**.

### 4.1 Functional requirements (what the system must do)

| ID | Requirement | Acceptance criterion |
|----|-------------|----------------------|
| FR1 | Load sales data | System reads `stores_sales_forecasting.csv` without crashing; missing/invalid rows are removed. |
| FR2 | Monthly aggregation | Data is aggregated to one row per calendar month for Sales and Quantity. |
| FR3 | Model training | Holt–Winters exponential smoothing (`ExponentialSmoothing` in statsmodels) is fitted on training data with additive trend and 12-month seasonality. |
| FR4 | Configurable horizon | User can request forecasts for 1–36 months (via script argument or chatbot). |
| FR5 | Dual targets | Both **Sales** (revenue) and **Quantity** (units) are forecast. |
| FR6 | Export results | Forecasts are written to `forecast_results.csv` with month index and predicted values. |
| FR7 | Visualisation | Historical vs forecast line charts are saved under `forecast_plots/`. |
| FR8 | Chatbot API | REST endpoints (`/api/chat`, `/api/statistics`, `/api/clear`) respond when the server is running. |
| FR9 | Web UI | Browser UI at `http://127.0.0.1:8000` allows message input and displays bot responses including tables and chart images. |
| FR10 | Dataset splits | Training, validation, and testing CSV files exist in `datasets/` after running `prepare_datasets.py`. |

### 4.2 Success criteria — measurable metrics

These metrics will be used to **review** the solution against the objectives (typically on the **test** set by training only on **train** data and tuning on **validation**).

| Metric | Target (success) | Notes |
|--------|------------------|-------|
| **MAPE** (Mean Absolute Percentage Error) on monthly Sales | ≤ 15% on test months | Primary accuracy measure for revenue forecast. |
| **MAPE** on monthly Quantity | ≤ 20% on test months | Quantity can be more volatile than revenue. |
| **RMSE** (Root Mean Square Error) | Lower than a naive baseline* | *Baseline: “next month = same as last month”. |
| **Data coverage** | ≥ 36 months of clean monthly data after aggregation | Ensures enough history for 12-month seasonality. |
| **Pipeline completion** | `python sales_forecasting.py` exits successfully and creates output files | Demonstrates end-to-end functionality. |
| **Chatbot response** | ≥ 90% of documented commands return a valid response within 30 seconds | Forecast, statistics, help, clear history. |
| **Usability** | Non-technical user can obtain a 12-month forecast via UI without editing code | Supports demo to company owner. |

*Exact figures can be recorded in Assignment Task 2 after evaluation; minor accuracy issues are acceptable per the brief.*

### 4.3 Non-functional requirements

| ID | Requirement |
|----|-------------|
| NFR1 | Runs on Windows with Python 3.10+ and dependencies in `requirements.txt`. |
| NFR2 | No requirement for paid cloud APIs (suitable for a small company demo). |
| NFR3 | Source code is readable and modular (`sales_forecasting.py`, `chatbot_backend.py`). |
| NFR4 | Personal/synthetic business data only — no live client PII in the prototype. |

---

## 5. Hypotheses to test and explore

| ID | Hypothesis | How it will be tested |
|----|------------|------------------------|
| H1 | Monthly retail sales show **seasonal patterns** repeating every 12 months. | Compare forecast model with seasonality vs without; inspect monthly plots. |
| H2 | **Holt–Winters exponential smoothing** is appropriate for this dataset size (~48 months). | Fit on training data; evaluate MAPE on validation and test splits. |
| H3 | Aggregating daily/line-level orders to **monthly totals** reduces noise and improves forecast stability. | Compare monthly MAPE to weekly aggregation (optional extension). |
| H4 | Forecasting **Sales** and **Quantity** separately improves interpretability for business users. | Review dual outputs in CSV and chatbot tables. |
| H5 | A **chatbot interface** makes the AI solution more demonstrable to non-technical clients than CLI-only tools. | Owner/staff trial: time to obtain first forecast via UI vs command line. |
| H6 | The model’s accuracy on the **held-out test months** (8 months) is acceptable for 12-month forward planning. | Calculate MAPE/RMSE on `datasets/test_monthly_sales.csv`. |

---

## 6. Data sources

### 6.1 Primary data source

| Field | Detail |
|-------|--------|
| **Name** | Store sales forecasting dataset |
| **File** | `stores_sales_forecasting.csv` |
| **Location** | Project root directory |
| **Type** | Structured transactional CSV (retail / e-commerce style) |
| **Access** | Local file — open licence for educational/prototype use |
| **Approx. size** | 2,121 order line records |
| **Date range** | January 2014 – December 2017 |
| **Key fields used** | `Order Date`, `Sales`, `Quantity` |

Additional columns (e.g. `Customer Name`, `Region`, `Category`) are available for future enhancements but are **not required** for the baseline monthly forecast model.

### 6.2 Suitability justification

- Contains **time-stamped sales** needed for forecasting.
- Covers **multiple years**, allowing 12-month seasonal modelling.
- Represents the type of data small business clients already hold (orders/export from POS or ecommerce).
- No API keys or paid subscriptions required — appropriate for an internship prototype.

### 6.3 Secondary / derived data sources

| Output | Description |
|--------|-------------|
| `datasets/train_monthly_sales.csv` | Monthly aggregates for model training |
| `datasets/validation_monthly_sales.csv` | Monthly aggregates for tuning/validation |
| `datasets/test_monthly_sales.csv` | Monthly aggregates for final evaluation |
| `forecast_results.csv` | Model predictions for future months |
| `forecast_plots/sales_quantity_forecast.png` | Visual evidence of historical vs predicted trends |

---

## 7. Data preparation

### 7.1 Preparation steps

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | **Load** CSV with UTF-8; fall back to Latin-1 encoding if needed | Handles special characters in text fields |
| 2 | **Parse dates** — `Order Date` converted to datetime | Required for time-based grouping |
| 3 | **Remove invalid rows** — drop rows missing Order Date, Sales, or Quantity | Prevents model errors |
| 4 | **Type coercion** — Sales and Quantity converted to numeric; non-numeric removed | Ensures mathematical operations work |
| 5 | **Aggregate** — group by calendar month; sum Sales and Quantity | Forecasting operates at monthly business planning level |
| 6 | **Sort** chronologically | Time series must be ordered in time |
| 7 | **Split** — chronological train / validation / test (no random shuffle) | Prevents data leakage from future into past |

Implementation: `load_sales_data()` and `build_monthly_series()` in `sales_forecasting.py`; split logic in `prepare_datasets.py`.

### 7.2 Data quality checks

- Confirm row count before and after cleaning.
- Confirm no duplicate month indices after aggregation.
- Confirm no negative Sales/Quantity values (or document treatment if present).
- Confirm continuous monthly coverage or document gaps.

### 7.3 Prepared data summary (after processing)

| Measure | Value |
|---------|-------|
| Raw transaction rows | 2,121 |
| Monthly observations | 48 months |
| Period | 2014-01 to 2017-12 |
| Features per month | Sales (revenue), Quantity (units) |

---

## 8. Training, validation and testing datasets

### 8.1 Split strategy

Time-series data must be split **in time order** (not randomly), so the model is never trained on future months.

| Dataset | Proportion | Months (approx.) | Role |
|---------|------------|------------------|------|
| **Training** | 70% | 33 months (Jan 2014 – Sep 2016) | Fit model parameters (level, trend, seasonality) |
| **Validation** | 15% | 7 months (Oct 2016 – Apr 2017) | Compare configurations; optional hyperparameter checks |
| **Testing** | 15% | 8 months (May 2017 – Dec 2017) | Final unbiased evaluation — **not** used during training |

### 8.2 How to generate evidence files

From the project folder:

```powershell
python prepare_datasets.py
```

This creates:

```
datasets/
├── train_monthly_sales.csv
├── validation_monthly_sales.csv
├── test_monthly_sales.csv
└── dataset_split_summary.csv
```

Include screenshots or copies of `dataset_split_summary.csv` in your portfolio as evidence.

### 8.3 How splits are used in the project

| Phase | Dataset used |
|-------|----------------|
| Prototype demo (`sales_forecasting.py` default) | All available monthly history for maximum forecast context |
| Rigorous evaluation (Assignment Task 2) | Train on `train_monthly_sales.csv`; tune on validation; report MAPE/RMSE on `test_monthly_sales.csv` |

Documenting both approaches is acceptable: the brief allows a functional solution with minor accuracy limitations while still requiring explicit train/validation/test datasets for Task 1 evidence.

---

## 9. AI model selection (overview for Task 1)

| Component | Choice |
|-----------|--------|
| **Problem type** | Supervised time-series forecasting |
| **Algorithm** | Holt–Winters triple exponential smoothing (`ExponentialSmoothing`) |
| **Library** | `statsmodels` (Python) |
| **Trend** | Additive |
| **Seasonality** | Additive, 12-month period |
| **Outputs** | Monthly Sales forecast, Monthly Quantity forecast |

**Why this model:** Interpretable, works well on short business histories, captures trend and yearly seasonality without needing deep learning or GPU infrastructure — suitable for a small software company prototype.

---

## 10. Evidence checklist (Task 1)

| Evidence required | Where to find it |
|-------------------|------------------|
| **Project objectives** | Sections 2–3 of this document |
| **Success criteria / functional requirements** | Section 4 |
| **Hypotheses** | Section 5 |
| **Data source identification** | Section 6 |
| **Data preparation description** | Section 7 |
| **Training dataset** | `datasets/train_monthly_sales.csv` (after running `prepare_datasets.py`) |
| **Validation dataset** | `datasets/validation_monthly_sales.csv` |
| **Testing dataset** | `datasets/test_monthly_sales.csv` |
| **Split summary** | `datasets/dataset_split_summary.csv` |

---

## 11. Review against objectives (initial self-assessment)

| Objective | Planned evidence |
|-----------|------------------|
| O1 Data readiness | `prepare_datasets.py` + `datasets/` folder |
| O2 Accurate forecasting | `forecast_results.csv`, MAPE on test set (Task 2) |
| O3 Seasonality | Model uses `seasonal_periods=12` |
| O4 Usable outputs | CSV + `forecast_plots/` |
| O5 Interactive demo | `chatbot_backend.py` + `static/` UI |
| O6 Evaluability | Metrics in Section 4.2 |
| O7 Deployability | `run_chatbot.ps1`, local FastAPI |

---

## 12. References (tools and libraries)

- pandas — data loading and aggregation  
- statsmodels — `ExponentialSmoothing` forecasting  
- matplotlib — chart generation  
- FastAPI / uvicorn — chatbot API server  
- Frontend — HTML, CSS, JavaScript (`static/`)

---

*This document satisfies Assignment Task 1: **Define the objectives of an AI project** for the Sales Forecasting AI demonstration.*
