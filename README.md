#### Stock API Project (FastAPI)

This project provides a high-performance RESTful API for retrieving stock market data using the `yfinance` library and `FastAPI` framework. The API includes endpoints for fetching stock summaries, historical data, news, financials, and more.

---

### Features
- Retrieve stock summaries, historical prices, and news articles.
- Access financial statements, institutional holdings, and analyst recommendations.
- Fetch peer companies, dividend history, earnings calendar, and stock splits.
- Get ESG/Sustainability scores, options chain, insider transactions, and company profiles.

---

### Endpoints

| Endpoint                          | Method | Description                     | Parameters                     |
|-----------------------------------|--------|---------------------------------|--------------------------------|
| `/stock/summary/{symbol}`         | GET    | Get summary data                | `symbol`: Stock ticker         |
| `/stock/historical/{symbol}/{timeframe}` | GET | Historical prices              | `symbol`, `timeframe`: 1D,1W, etc. |
| `/stock/news/{symbol}`            | GET    | News articles                   | `symbol`                       |
| `/stock/financials/{symbol}`      | GET    | Financial statements            | `symbol`                       |
| `/stock/holdings/{symbol}`        | GET    | Institutional holdings          | `symbol`                       |
| `/stock/analysis/{symbol}`        | GET    | Analyst recommendations         | `symbol`                       |
| `/stock/peers/{symbol}`           | GET    | Peer companies                  | `symbol`                       |
| `/stock/dividends/{symbol}`       | GET    | Dividend history                | `symbol`                       |
| `/stock/earnings/{symbol}`        | GET    | Earnings calendar               | `symbol`                       |
| `/stock/splits/{symbol}`          | GET    | Stock splits history            | `symbol`                       |
| `/stock/sustainability/{symbol}`  | GET    | ESG/Sustainability scores       | `symbol`                       |
| `/stock/options/{symbol}`         | GET    | Options chain                   | `symbol`                       |
| `/stock/insider/{symbol}`         | GET    | Insider transactions            | `symbol`                       |
| `/stock/profile/{symbol}`         | GET    | Company profile/overview        | `symbol`                       |
| `/stock/search`                   | GET    | Search for stock by name        | `q`: Query string               |

---

### Getting Started

#### Prerequisites
- Python 3.7 or higher
- `pip` (Python package manager)

#### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/stock-api-yahoo.git
   cd stock-api-yahoo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Running the Application

1. Start the FastAPI server:
   ```bash
   python app.py
   ```

2. The API will be available at:
   ```plaintext
   http://127.0.0.1:8000
   ```

#### Interactive API Documentation

FastAPI automatically generates interactive API documentation. Access them at:

- **Swagger UI (Recommended)**: 
  ```plaintext
  http://127.0.0.1:8000/docs
  ```
  Interactive API explorer where you can test all endpoints directly.

- **ReDoc (Alternative)**:
  ```plaintext
  http://127.0.0.1:8000/redoc
  ```
  Beautiful, readable API documentation.

- **OpenAPI JSON Schema**:
  ```plaintext
  http://127.0.0.1:8000/openapi.json
  ```
  Raw OpenAPI specification for integration with other tools.

---

### Example Usage

- **Get Stock Summary**:
  ```plaintext
  GET /stock/summary/AAPL
  ```

- **Get Historical Data**:
  ```plaintext
  GET /stock/historical/AAPL/1M
  ```

- **Get News Articles**:
  ```plaintext
  GET /stock/news/AAPL
  ```

- **Search Stock by Company Name**:
  ```plaintext
  GET /stock/search?q=Apple
  ```

---

### API Response Examples

#### Stock Summary
```json
{
  "previousClose": 238.15,
  "open": 238.85,
  "bid": 238.95,
  "ask": 238.96,
  "daysRange": "237.50 - 240.25",
  "52WeekRange": "164.08 - 254.99",
  "volume": 38505600,
  "avgVolume": 52391100,
  "marketCap": 2410000000000,
  "beta": 1.24,
  "peRatio": 31.45,
  "eps": 7.61,
  "dividendYield": 0.0043,
  "targetEstimate": 245.50
}
```

#### Stock Search
```json
{
  "symbol": "AAPL",
  "longName": "Apple Inc.",
  "previousClose": 238.15,
  "open": 238.85,
  ...
}
```

---

### Contributing
Feel free to submit issues or pull requests to improve the project.

---

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---