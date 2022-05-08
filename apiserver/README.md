API server for a ML-model
==============================


Preparing a random ML-model for deployment
------------

1. Take a Jupyter Notebook with ML-model. See an example in notebooks/raw/churn_dataset_analysis.ipynb

2. Run the source Jupyter Notebook code, making the necessary adjustments, reproducing and saving the model, scalers and encoders locally. See an example in notebooks/processed/churn_dataset_analysis.ipynb

3. Load the model, scalers and encoders obtained at the previous step into MlFlow. (You will need to provide access data to the cloud S3 bucket). See an example in notebooks/processed/log_model.ipynb

4. Prepare an API server for the resulting model using FastAPI and Pydantic.


_____


Project Organization
------------

    ├── README.md                     <- 
    ├── docker-compose.yaml           <- 
    ├── Dockerfile                    <- 
    ├── entrypoint.sh                 <- 
    ├── requirements.txt              <- 
    ├── example.env                   <- 
    ├── main.py                       <- 
    │
    ├── app                           <- 
    │   ├── __init__.py               <- 
    │   ├── api.py                    <- 
    │   ├── handlers.py               <- 
    │   │
    │   ├── forms                     <- 
    │   │   ├── __init__.py           <- 
    │   │   ├── AnswerData.py         <- 
    │   │   └── PredictionData.py     <- 
    │   │   
    │   └── modules                   <- 
    │       ├── __init__.py           <- 
    │       ├── ModelProcessing.py    <- 
    │       └── TokenVerification.py  <- 
    │
    ├── tests                         <- 
    │   ├── __init__.py               <- 
    │   ├── test_ModelProcessing.py   <- 
    │   └── test_TokenVerification.py <- 
    │
    ├── data                          <- 
    │   │
    │   └── raw                       <- 
    │       └── *.scv                 <-     
    │
    ├── notebooks                     <- 
    │   │
    │   ├── raw                       <- 
    │   │   └── *.ipnb                <- 
    │   │
    │   └── processed                 <- 
    │       └── *.ipnb                <- 
    │
    └── models                        <- 

------------