# STOCK NEWS SCRAPPING ETL PIPLINE

## Project Overview :
Developed an end-to-end ETL pipeline for a small financial trading firm to automate the scraping of stock news articles from multiple websites. The solution initially scraped 300,000+ articles from ~9,000 pages to establish a comprehensive historical dataset. Using Apache Airflow, the pipeline schedules scraping tasks every 2 hours to fetch the latest news, ensuring up-to-date insights. Data is stored in an on-premise PostgreSQL database with robust deduplication logic to prevent duplicate entries. The entire pipeline is containerized with Docker, enabling seamless deployment and scalability, delivering accurate, timely data to support informed trading decisions.

![Python 3.10](https://img.shields.io/badge/Python-3.10-yellow.svg)
![Asyncio](https://img.shields.io/badge/Asyncio-Async%20Programming-red.svg)
![Multithreading](https://img.shields.io/badge/Multithreading-Concurrency-green.svg)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Task%20Orchestration-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Containerization-brightblue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-yellowgreen.svg)


### Key Metrics :
- Initial ingestion of **300,000+** articles from **10,000+** pages.
- Automated daily scraping of **1,000+** articles.
- Scraping speed improved by **65%** using asynchronous programming.
- Reduced response times by **10x** with optimized proxy rotation.

## Architecture Diagram:
![stock_news_etl_pipeline_(containerized)](https://github.com/user-attachments/assets/91d457f0-549b-4ad5-9197-adab6245b524)

## Tech Stack :

| Component         | Technology Used                |
|-------------------|--------------------------------|
| **Programming**   | Python (`asyncio`, `requests`) |
| **Task Scheduler**| Apache Airflow                 |
| **Database**      | PostgreSQL                     |
| **Containerization** | Docker                      |
| **Libraries**     | BeautifulSoup, psycopg2, logging |
| **Tools**         | IP Proxy Rotation              |

## Screenshots :
![docker_shot](https://github.com/user-attachments/assets/5dab9458-e52d-4ab1-85a6-5ba10f80a4e0)
![investing_log_shot](https://github.com/user-attachments/assets/8263a2de-7064-4c96-90a0-cadbec52f3bc)
![money_log_shot](https://github.com/user-attachments/assets/7d77879f-d510-4e64-81eb-80c2427e29fb)
