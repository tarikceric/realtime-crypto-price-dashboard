# realtime-crypto-price-dashboard

***under developement - currently fetches stock data

Developing a dashboard powered by real-time streaming of cryptocurrency prices into QuestDB

# Setup
- Replace API key in .env with own key
- install requirements
- docker-compose up
- Populate the DB: python -m celery --app app.worker.celery_app worker --beat -l info -c 1
  - view here: http://127.0.0.1:9000
- Stream to dashboard: PYTHONPATH=. python app/main.py
  - view here: http://127.0.0.1:8050/
 
# Tools
- Docker
- Redis
- QuestDB
- Celery
- Plotly
- Dash

## Main Components
Backend:
- Utilizes docker for Redis and QuestDB
- Triggers Celery workers to use a Redis broker and retrieve data from an api
- Stores the data into QuestDB

Frontend:
- Grab data from QuestDB and visualize via Plotly and Dash

Based on https://hackernoon.com/build-a-real-time-stock-price-dashboard-with-python-questdb-and-plotly
