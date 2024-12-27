from typing import Optional
from phi.tools.base import BaseTool
import yfinance as yf


class DebtToEquityRatioTool(BaseTool):
    """Tool to calculate Debt to Equity Ratio for a given stock symbol"""

    name: str = "debt_to_equity_ratio"
    description: str = "Calculate the Debt to Equity ratio for a given stock symbol"
    parameters: dict = {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)",
        }
    }

    async def run(self, symbol: str) -> str:
        try:
            # Get the stock information
            stock = yf.Ticker(symbol)
            
            # Get the balance sheet data
            balance_sheet = stock.balance_sheet
            
            if balance_sheet.empty:
                return f"Could not retrieve balance sheet data for {symbol}"
            
            # Get the most recent data
            latest_data = balance_sheet.iloc[:, 0]
            
            # Calculate total debt (short-term + long-term debt)
            total_debt = (
                latest_data.get('Short Long Term Debt', 0) +
                latest_data.get('Long Term Debt', 0)
            )
            
            # Get total stockholders equity
            total_equity = latest_data.get('Stockholders Equity', 0)
            
            if total_equity == 0:
                return f"Cannot calculate Debt to Equity ratio for {symbol} - Total Equity is 0"
            
            # Calculate Debt to Equity ratio
            debt_to_equity = total_debt / total_equity
            
            return {
                "symbol": symbol,
                "total_debt": total_debt,
                "total_equity": total_equity,
                "debt_to_equity_ratio": round(debt_to_equity, 2),
                "date": str(balance_sheet.columns[0].date())
            }
            
        except Exception as e:
            return f"Error calculating Debt to Equity ratio for {symbol}: {str(e)}"


class QuickRatioTool(BaseTool):
    """Tool to calculate Quick Ratio (Acid Test) for a given stock symbol"""

    name: str = "quick_ratio"
    description: str = "Calculate the Quick Ratio (Acid Test) for a given stock symbol"
    parameters: dict = {
        "symbol": {
            "type": "string",
            "description": "Stock symbol (e.g., AAPL, MSFT)",
        }
    }

    async def run(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            balance_sheet = stock.balance_sheet
            
            if balance_sheet.empty:
                return f"Could not retrieve balance sheet data for {symbol}"
            
            latest_data = balance_sheet.iloc[:, 0]
            
            # Calculate quick assets (current assets - inventory)
            current_assets = latest_data.get('Total Current Assets', 0)
            inventory = latest_data.get('Inventory', 0)
            quick_assets = current_assets - inventory
            
            # Get current liabilities
            current_liabilities = latest_data.get('Total Current Liabilities', 0)
            
            if current_liabilities == 0:
                return f"Cannot calculate Quick Ratio for {symbol} - Current Liabilities is 0"
            
            # Calculate Quick Ratio
            quick_ratio = quick_assets / current_liabilities
            
            return {
                "symbol": symbol,
                "quick_assets": quick_assets,
                "current_liabilities": current_liabilities,
                "quick_ratio": round(quick_ratio, 2),
                "date": str(balance_sheet.columns[0].date())
            }
            
        except Exception as e:
            return f"Error calculating Quick Ratio for {symbol}: {str(e)}"