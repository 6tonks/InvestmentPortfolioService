from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service
from flask import abort


class ViewUserStocksResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_portfolio(cls, user_id):
        stocks = d_service.get_by_prefix_not_zero('investmentportfolios', 'all', 'user_id', user_id, 'quantity')
        if not stocks:
            abort(400, str({'user_id': ['No stocks for the requested user.']}))
        res = {}
        for stock in stocks:
            res[stock['ticker']] = stock['quantity']
        return res, 200

    @classmethod
    def get_stock_shares(cls, user_id, ticker):
        res = d_service.get_by_two_prefix('investmentportfolios', 'all', 'user_id', user_id, 'ticker', ticker)
        if not res:
            abort(400, str({'ticker': ['No shares for the requested stock.']}))
        return res
