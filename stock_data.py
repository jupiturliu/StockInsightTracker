import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol: str, period: str = "1y") -> tuple:
    """
    Fetch stock data for a given symbol and period.
    
    Args:
    symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
    period (str): Time period for historical data (default: '1y')
    
    Returns:
    tuple: (DataFrame with stock data, dict with company info)
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        
        if df.empty:
            return None, None
        
        # Round float columns to 2 decimal places
        float_columns = df.select_dtypes(include=['float64']).columns
        df[float_columns] = df[float_columns].round(2)
        
        info = get_company_info(stock)
        return df, info
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

def get_company_info(stock: yf.Ticker) -> dict:
    """
    Get relevant company information from a yfinance Ticker object.
    
    Args:
    stock (yf.Ticker): yfinance Ticker object
    
    Returns:
    dict: Dictionary containing relevant company information
    """
    info = stock.info
    return {
        'longName': info.get('longName', 'N/A'),
        'sector': info.get('sector', 'N/A'),
        'industry': info.get('industry', 'N/A'),
        'website': info.get('website', 'N/A'),
        'currentPrice': info.get('currentPrice', 'N/A'),
        'marketCap': info.get('marketCap', 'N/A'),
        'trailingPE': info.get('trailingPE', 'N/A'),
        'forwardPE': info.get('forwardPE', 'N/A'),
        'pegRatio': info.get('pegRatio', 'N/A'),
        'priceToBook': info.get('priceToBook', 'N/A'),
        'enterpriseToRevenue': info.get('enterpriseToRevenue', 'N/A'),
        'enterpriseToEbitda': info.get('enterpriseToEbitda', 'N/A'),
    }
