# Python End-to-End ETL Pipeline Project

This project is an end-to-end ETL data engineering pipeline built using Python, following scalable Medallion Architecture principles and production-oriented engineering practices.

The pipeline ingests stock market data from the Alpha Vantage API, processes and transforms the data through multiple ETL layers, stores it in a relational database, and exposes insights through an interactive dashboard.

## Architecture Overview
This project follows a **3-layer ETL architecture inspired by the Medallion Architecture pattern**:

- **Ingestion Layer (Bronze)**  
  Responsible for extracting raw stock market data from the Alpha Vantage API and loading it into the database for further processing.

- **Transformation Layer (Silver)**  
  Responsible for cleaning, transforming, and structuring the raw data into processed tables that serve as the foundation for analytics.

- **Serving Layer (Gold)**  
  Responsible for creating business-ready, one-to-one analytical views optimized for dashboard consumption.

The **Streamlit dashboard is built directly on top of the Serving (Gold) layer**, ensuring separation between raw ingestion, transformation logic, and presentation/reporting.

## Tech Stack :
- Python — ETL orchestration, data processing, API integration
- MySQL — storage for all 3 layers 
- Streamlit — interactive dashboard and data visualization
- Alpha Vantage API

## Project Highlights :
- End-to-end ETL pipeline implementation
- API-based data ingestion
- Multi-layer data processing using Medallion Architecture concepts
- Modular and maintainable Python project structure
- Production-style practices including configuration management, error handling, and separation of concerns
- Interactive dashboard for analytics and reporting

## Live Dashboard Link :
###  https://python-etl-project-rtff47gxug6aqcegxowh4x.streamlit.app/

<img width="1408" height="835" alt="Screenshot 2026-07-08 at 12 20 46 PM" src="https://github.com/user-attachments/assets/a7ea9e5b-5730-4918-822f-bcde9df6f55b" />

<img width="1405" height="839" alt="Screenshot 2026-07-08 at 12 21 08 PM" src="https://github.com/user-attachments/assets/4f28aeb2-edd6-49ad-83e4-ddd3aff2c6a8" />



## Notes :
- This project uses the free Alpha Vantage API tier, which has request rate limitations.
- Dashboard refresh may take 45–60 seconds depending due to free tier limitations.
- Free tier limit: 25 API requests per day
