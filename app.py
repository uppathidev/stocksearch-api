from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import yfinance as yf
import requests
import json
import math
from typing import Any

app = FastAPI()


# Helper function to convert NaN and Inf values to None for JSON serialization
def convert_nan_inf_to_none(obj: Any) -> Any:
    """Recursively convert NaN and Inf values to None."""
    if isinstance(obj, dict):
        return {key: convert_nan_inf_to_none(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_nan_inf_to_none(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    else:
        return obj


# Helper: Find ticker symbol from company name using Yahoo search
def search_symbol_from_name(query):
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {
        "q": query,
        "quotesCount": 1,
        "newsCount": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    quotes = data.get("quotes")
    if quotes and len(quotes) > 0:
        return quotes[0].get("symbol")
    return None

@app.get('/stock/search')
def get_stock_search(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    symbol = search_symbol_from_name(q)
    if not symbol:
        raise HTTPException(status_code=404, detail="No matching stock found")

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        result = {
            "symbol": symbol,
            "longName": info.get('longName'),
            "previousClose": info.get('previousClose'),
            "open": info.get('open'),
            "bid": info.get('bid'),
            "ask": info.get('ask'),
            "daysRange": f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
            "52WeekRange": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
            "volume": info.get('volume'),
            "avgVolume": info.get('averageVolume'),
            "marketCap": info.get('marketCap'),
            "beta": info.get('beta'),
            "peRatio": info.get('trailingPE'),
            "eps": info.get('trailingEps'),
            "earningsDate": str(info.get('earningsDate')),
            "dividendYield": info.get('dividendYield'),
            "targetEstimate": info.get('targetMeanPrice')
        }
        return convert_nan_inf_to_none(result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/stock/summary/{symbol}')
def get_stock_summary(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        result = {
            "previousClose": info.get('previousClose'),
            "open": info.get('open'),
            "bid": info.get('bid'),
            "ask": info.get('ask'),
            "daysRange": f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
            "52WeekRange": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
            "volume": info.get('volume'),
            "avgVolume": info.get('averageVolume'),
            "marketCap": info.get('marketCap'),
            "beta": info.get('beta'),
            "peRatio": info.get('trailingPE'),
            "eps": info.get('trailingEps'),
            "earningsDate": info.get('earningsDate'),
            "dividendYield": info.get('dividendYield'),
            "targetEstimate": info.get('targetMeanPrice')
        }
        return convert_nan_inf_to_none(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/historical/{symbol}/{timeframe}')
def get_historical_data(symbol: str, timeframe: str):
    try:
        period_map = {
            '1D': '1d', '1W': '5d', '1M': '1mo',
            '3M': '3mo', '1YR': '1y', '3YR': '3y',
            '5YR': '5y', 'ALL': 'max'
        }
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period_map.get(timeframe, '1y'), interval='1d')
        result = hist.reset_index().to_dict(orient='records')
        return convert_nan_inf_to_none(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/news/{symbol}')
def get_stock_news(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        news = stock.news

        # Check if news is empty
        if not news:
            raise HTTPException(status_code=404, detail="No news available for the given stock.")

        return convert_nan_inf_to_none(news)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/financials/{symbol}')
def get_financials(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        result = {
            "income_stmt": stock.income_stmt.to_dict(),
            "balance_sheet": stock.balance_sheet.to_dict(),
            "cash_flow": stock.cashflow.to_dict()
        }
        return convert_nan_inf_to_none(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/holdings/{symbol}')
def get_holdings(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        result = {
            "institutional_holders": stock.institutional_holders.to_dict(),
            "major_holders": stock.major_holders.to_dict()
        }
        return convert_nan_inf_to_none(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/analysis/{symbol}')
def get_analysis(symbol: str):
    try:
        stock = yf.Ticker(symbol)

        # Convert recommendations and earnings_dates to dictionaries with string keys
        recommendations = stock.recommendations.reset_index().to_dict(orient='records')
        earnings_estimates = stock.earnings_dates.reset_index().to_dict(orient='records')

        result = {
            "recommendations": recommendations,
            "earnings_estimates": earnings_estimates
        }
        return convert_nan_inf_to_none(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/stock/peers/{symbol}')
def get_peers(symbol: str):
    try:
        api_key = 'd0ounq9r01qr8ds0dhvgd0ounq9r01qr8ds0di00'
        url = f'https://finnhub.io/api/v1/stock/peers?symbol={symbol}&token={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            peers = response.json()
            # Remove the symbol itself from the list
            peers = [peer for peer in peers if peer != symbol.upper()]
            return {"peers": peers}
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch peers")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/dividends/{symbol}')
def get_dividends(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        dividends = stock.dividends.reset_index().to_dict(orient='records')
        return convert_nan_inf_to_none(dividends)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get('/stock/earnings/{symbol}')
def get_earnings(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        earnings = stock.earnings_dates.reset_index().to_dict(orient='records')
        return convert_nan_inf_to_none(earnings)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/splits/{symbol}')
def get_splits(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        splits = stock.splits.reset_index().to_dict(orient='records')
        return convert_nan_inf_to_none(splits)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/sustainability/{symbol}')
def get_sustainability(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        try:
            sustainability = stock.sustainability
            if sustainability is None or (isinstance(sustainability, dict) and len(sustainability) == 0):
                raise HTTPException(status_code=404, detail="Sustainability data not available for this stock")
            return convert_nan_inf_to_none(sustainability.to_dict() if hasattr(sustainability, 'to_dict') else sustainability)
        except HTTPException:
            raise
        except Exception as inner_e:
            # Sustainability data may not be available for all stocks
            raise HTTPException(status_code=404, detail=f"Sustainability data not available for this stock")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/options/{symbol}')
def get_options(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        expirations = stock.options
        options_chain = {}
        for date in expirations:
            options_chain[date] = {
                "calls": stock.option_chain(date).calls.to_dict(orient='records'),
                "puts": stock.option_chain(date).puts.to_dict(orient='records')
            }
        return convert_nan_inf_to_none(options_chain)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/insider/{symbol}')
def get_insider(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        insider = stock.insider_transactions.reset_index().to_dict(orient='records')
        return convert_nan_inf_to_none(insider)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/stock/profile/{symbol}')
def get_profile(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract CEO name from companyOfficers
        ceo_name = None
        company_officers = info.get("companyOfficers", [])
        for officer in company_officers:
            if "title" in officer and "CEO" in officer["title"]:
                ceo_name = officer.get("name")
                break

        profile = {
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "website": info.get("website"),
            "description": info.get("longBusinessSummary"),
            "ceo": ceo_name,
            "city": info.get("city"),
            "country": info.get("country"),
        }
        return convert_nan_inf_to_none(profile)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
