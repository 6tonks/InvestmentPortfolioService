from marshmallow import Schema, fields
from flask import abort
from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class BuySellSchema(Schema):
    user_id = fields.Integer(required=True)
    ticker = fields.String(required=True)
    quantity = fields.Integer(required=True)


class BuySellResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def buy_stocks(cls, order_args):
        user_id = order_args['user_id']
        ticker = order_args['ticker']
        quantity = order_args['quantity']
        res = d_service.create_or_update_stock_in_portfolio("investmentportfolios", user_id, ticker, quantity)
        return res


    @classmethod
    def sell_stocks(cls, order_args):
        user_id = order_args['user_id']
        ticker = order_args['ticker']
        sell_quantity = int(order_args['quantity'])
        stock_in_db = d_service.get_by_prefix('investmentportfolios', user_id, 'ticker', ticker)
        available_quantity = stock_in_db[0]['quantity']
        if sell_quantity > available_quantity:
            abort(400, str({'quantity': ['Not enough shares in user portfolio.']}))
        res = d_service.sell_stock_in_portfolio("investmentportfolios", user_id, ticker, sell_quantity)
        return res
