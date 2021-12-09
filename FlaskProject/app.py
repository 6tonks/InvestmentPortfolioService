from flask import Flask, request, abort, Response, json
from flask_restful import Resource, Api
from flask_cors import CORS
import utils.rest_utils as rest_utils
from application_services.TransactionsResource.buy_sell_resource import BuySellSchema, BuySellResource
from application_services.ViewResource.view_user_stocks import ViewUserStocksResource

app = Flask(__name__)
CORS(app)
api = Api(app)
buy_sell_schema = BuySellSchema()


class WelcomePage(Resource):
    def get(self):
        return {"Welcome": 'Investment Portfolio Service',
                "links": [
                    {
                        'rel': 'User portfolio',
                        'method': 'GET',
                        'href': f'/api/user/<_id>'
                    },
                    {
                        'rel': 'User stock quantity',
                        'method': 'GET',
                        'href': f'/api/user/<_id>/stock/<_ticker>'
                    },
                    {
                        'rel': 'Buy shares',
                        'method': 'POST',
                        'href': f'/api/buy/<_id>'
                    },
                    {
                        'rel': 'Sell shares',
                        'method': 'POST',
                        'href': f'/api/sell/<_id>'
                    }
                 ]
                }


class BuyStock(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        payload = r_json["data"]
        
        # AWS Step Function can only send string request
        payload["user_id"] = _id
        payload["quantity"] = int(payload["quantity"])
        
        errors = buy_sell_schema.validate(payload)
        if errors:
            abort(400, str(errors))
        res, status = BuySellResource.buy_stocks(payload)
        if status == 201 and not res:
            res = {'success': 1,
                   'links': BuySellResource.default_links(_id, payload["ticker"])
                  }
        rsp = Response(json.dumps(res), status=201, content_type="application/json")
        return rsp


class SellStock(Resource):
    def post(self, _id: int):
        inputs = rest_utils.RESTContext(request)
        r_json = inputs.to_json()
        payload = r_json["data"]
        
        # AWS Step Function can only send string request
        payload["user_id"] = _id
        payload["quantity"] = int(payload["quantity"])

        errors = buy_sell_schema.validate(payload)
        if errors:
            abort(400, str(errors))
        res, status = BuySellResource.sell_stocks(payload)
        if status == 201 and not res:
            res = {'success': 1,
                   'links': BuySellResource.default_links(_id, payload["ticker"])
                  }
        rsp = Response(json.dumps(res), status=201, content_type="application/json")
        return rsp


class UserPortfolio(Resource):
    def get(self, _id: int):
        res = {}
        res["portfolio"], status = ViewUserStocksResource.get_portfolio(_id)
        if status == 200:
            res["user"] = _id
            res["self"] = f'/api/user/{_id}'
        rsp = Response(json.dumps(res, default=str), status=status, content_type="application/json")
        return rsp


class UserStockShares(Resource):
    def get(self, _id: str, _ticker: str):
        res = ViewUserStocksResource.get_stock_shares(_id, _ticker)[0]
        res["self"] = f'/api/user/{_id}/stock/{_ticker}'
        res["links"] = [
                    {
                        'rel': 'user',
                        'href': f'/api/user/{_id}'
                    }
                ]
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

# Removing the last slash to solve 308 redirect problem
api.add_resource(WelcomePage, '/')
api.add_resource(BuyStock, '/api/buy/<int:_id>')
api.add_resource(SellStock, '/api/sell/<int:_id>')
api.add_resource(UserPortfolio, '/api/user/<int:_id>')
api.add_resource(UserStockShares, '/api/user/<int:_id>/stock/<string:_ticker>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8081")
