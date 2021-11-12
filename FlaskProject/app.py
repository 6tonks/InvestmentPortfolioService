from flask import Flask, request, abort
from flask_restful import Resource, Api
from application_services.TransactionsResource.buy_sell_resource import BuySellSchema, BuySellResource

app = Flask(__name__)
api = Api(app)
schema = BuySellSchema()


class BuyStock(Resource):
    def get(self):
        buy_args = request.args
        errors = schema.validate(buy_args)
        if errors:
            abort(400, str(errors))
        res = BuySellResource.buy_stocks(buy_args)
        return "", 204


api.add_resource(BuyStock, '/api/buy/')


#@app.before_request
#def before_request_func():
#    result_ok = simple_security.check_security(request)
#
#    if not result_ok:
#        return {"Error": "Invalid authentication token"}, 401


@app.route('/')
def hello_world():
    return 'Welcome to Investment Portfolio Service!'


@app.route('/api/user/sell/')
def sell_stocks():
    return 'sell stocks'


@app.route('/api/user/view/ ')
def view_user_portfolio():
    return 'view portfolio'


if __name__ == '__main__':
    app.run(debug=True)
