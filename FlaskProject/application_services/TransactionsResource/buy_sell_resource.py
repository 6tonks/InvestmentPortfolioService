from marshmallow import Schema, fields
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
    def buy_stocks(cls, buy_args):
        user_id = buy_args['user_id']
        ticker = buy_args['ticker']
        quantity = buy_args['quantity']
        res = d_service.create_or_update_stock_in_portfolio("investmentportfolios", user_id, ticker, quantity)
        return res