from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, InsiderTrading

class TradingStrategy(Strategy):

    def __init__(self):
        # Focus on AAPL for this strategy
        self.ticker = "AAPL"
        # Data sources: social sentiment and insider trading
        self.data_list = [SocialSentiment(self.ticker), InsiderTrading(self.ticker)]

    @property
    def interval(self):
        """
        Utilizing daily data for analysis.
        """
        return "1day"

    @property
    def assets(self):
        """
        The trading strategy is focused on Apple.
        """
        return [self.ticker]

    @property
    def data(self):
        """
        Data used includes social sentiment and insider trading for AAPL.
        """
        return self.data_list

    def run(self, data):
        """
        Implements the trading logic based on social sentiment and insider trades.
        """
        allocation = 0.5  # Default allocation

        # Analyzing the sentiment data.
        sentiment_data = data[("social_sentiment", self.ticker)]
        if sentiment_data and len(sentiment_data) > 0:
            recent_sentiment = sentiment_data[-1]["twitterSentiment"]
            # Positive sentiment increases allocation
            if recent_sentiment > 0.5:
                allocation += 0.2
            else:
                allocation -= 0.2

        # Checking for recent insider trading activity.
        insider_data = data[("insider_trading", self.ticker)]
        if insider_data and len(insider_data) > 0:
            recent_trades = insider_data[-1]["transactionType"]
            # Insider sales reduce allocation
            if "Sale" in recent_trades:
                allocation = max(0, allocation - 0.3)  # Avoid negative allocation

        # Ensure allocation remains within 0 and 1.
        allocation = min(max(allocation, 0), 1)

        return TargetAllocation({self.ticker: allocation})