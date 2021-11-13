from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service
from flask import abort


class ViewUserStocksResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_portfolio(cls, user_id):
        res = d_service.get_table_not_zero("investmentportfolios", user_id, "quantity")
        if not res:
            abort(400, str({'user_id': ['No stocks for the requested user.']}))
        return res

    @classmethod
    def get_stock_shares(cls, user_id, ticker):
        res = d_service.get_by_prefix("investmentportfolios", user_id, "ticker", ticker)
        if not res:
            abort(400, str({'ticker': ['No shares for the requested stock.']}))
        return res
