from flask import Flask, request, abort, Response, json
from flask_restful import Resource, Api
from application_services.TransactionsResource.buy_sell_resource import BuySellSchema, BuySellResource
from application_services.ViewResource.view_user_stocks import ViewUserStocksResource

app = Flask(__name__)
api = Api(app)
buy_sell_schema = BuySellSchema()


class BuyStock(Resource):
    def get(self):
        errors = buy_sell_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        res = BuySellResource.buy_stocks(request.args)
        return "", 204


class SellStock(Resource):
    def get(self):
        errors = buy_sell_schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        res = BuySellResource.sell_stocks(request.args)
        return "", 204


class UserPortfolio(Resource):
    def get(self, _id: str):
        res = ViewUserStocksResource.get_portfolio(_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


class UserStockShares(Resource):
    def get(self, _id: str, _ticker: str):
        res = ViewUserStocksResource.get_stock_shares(_id, _ticker)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


api.add_resource(BuyStock, '/api/buy/')
api.add_resource(SellStock, '/api/sell/')
api.add_resource(UserPortfolio, '/api/user/<string:_id>/')
api.add_resource(UserStockShares, '/api/user/<string:_id>/stock/<string:_ticker>/')


@app.route('/')
def hello_world():
    return 'Welcome to Investment Portfolio Service!'


if __name__ == '__main__':
    app.run(debug=True)
