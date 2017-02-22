from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

user={"username": "00000000",
	  "password": "password"}
favStocks={"userId": "00000000",
		   "stockInfoSymbol": "GOOG"}
stock={"name": "Richard Cranium",
	   "sector": "SECTOR",
	   "industry": "Technology",
	   "earnings": "11.11",
	   "earningsGrowth": "22.22",
	   "sales": "33.33",
	   "cashFlow": "44.44",
	   "bookValue": "55.55",
	   "debtEquity": "66.66",
	   "returnEquity": "77.77",
	   "returnAssets": "88.88",
	   "profitMargin": "99.99",
	   "dividendPayout": "10.10",
	   "assetsLiabilities": "12.12",
	   "quick": "13.13",
	   "interestCoverage": "14.14",
	   "assetTurnover": "15.15",
	   "inventoryTurnover": "16.16",
	   "dividendYield": "17.17"}
dailyStocks={"stockInfoSymbol": "GOOG",
			 "closeDate": "2017-01-013",
			 "closePrice": "555.55"}
prediction={"stockInfoSymbol": "GOOG",
			"predictShort": "Gainz",
			"predictMedium": "Lozzes",
			"predictLong": "Disappointment"}

class user(Resource):
	def get(self):
		return user

	def put(self):
		return user

class followedStocks(Resource):
	def get(self):
		return favStocks

	def put(self):
		return favStocks

class stock(Resource):
	def get(self):
		return stock

	def put(self):
		return stock

class daily(Resource):
	def get(self):
		return favStocks

	def put(self):
		return favStocks

class prediction(Resource):
	def get(self):
		return prediction

	def put(self):
		return prediction

api.add_resource(user, '/user')
api.add_resource(followedStocks, '/favorite')
api.add_resource(stock, '/stock')
api.add_resource(daily, '/daily')
api.add_resource(prediction, '/predict')


if __name__ == '__main__':
	app.run(debug=True)

