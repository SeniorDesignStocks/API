from flask import Flask, request
from flask_restful import Resource, Api
import pyodbc
import bcrypt
import json

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=JON;DATABASE=stocksSimplified;')
#print("Connected to database.")

app = Flask(__name__)
api = Api(app)

#TODO:
#	Implement some sort of security
#	Refactor code


Users={"UserID": "00000000",
	  "UserName": "Richard Cranium",
	  "Password": "password",
	  "Email": "richard@cranium.com"}
Followed_Stocks={"UserID": "00000000",
		   "Symbol": "GOOG"}
Stock_Info={"Symbol": "GOOG",
		"Name": "Richard Cranium",
	   "Sector": "SECTOR",
	   "Industry": "Technology",
	   "Price To Earnings": "11.11",
	   "Price To Earnings Growth": "22.22",
	   "Price To Sales": "33.33",
	   "Price To Cash Flow": "44.44",
	   "Price To Book Value": "55.55",
	   "Debt To Equity": "66.66",
	   "Return On Equity": "77.77",
	   "Return On Assets": "88.88",
	   "Profit Margin": "99.99",
	   "Dividend Payout": "10.10",
	   "Current Assets To Liabilities": "12.12",
	   "Quick": "13.13",
	   "Interest Coverage": "14.14",
	   "Asset Turnover": "15.15",
	   "Inventory Turnover": "16.16",
	   "Dividend Yield": "17.17"}
Daily_Stocks={"Symbol": "GOOG",
			 "CloseDate": "2017-01-013",
			 "ClosePrice": "555.55",
			 "TransactionID": "01010101"}
Prediction_Cache={"Symbol": "GOOG",
			"Prediction Short": "Gainz",
			"Prediction Medium": "Lozzes",
			"Prediction Long": "Disappointment"}

class test(Resource):
	def get(self):
		return "This is a test endpoint"

class user(Resource):
	def get(self):
		inputUsername = request.args.get('username')
		inputPassword = request.args.get('password')

		userSQL = "SELECT UserName, Password, Salt FROM Users;"
		cursor = cnxn.cursor()
		cursor.execute(userSQL)
		user = cursor.fetchall()
		userList = []

		for i in user:
			userList.append([i[0], i[1], str(i[2])])
		for i in userList:
			if i[0] == inputUsername:
				if bcrypt.checkpw(inputPassword.encode('utf-8'), i[1]):
					return "Login Successful"
		
		return "Invalid Username/Password"
	def put(self):
		inputUsername = request.args.get('username')
		inputPassword = request.args.get('password')
		inputEmail = request.args.get('email')

		userSQL = "SELECT UserID, UserName, Password, Email, Salt FROM Users;"
		cursor = cnxn.cursor()
		cursor.execute(userSQL)
		user = cursor.fetchall()
		userList = []
		userid = 1
		for i in user:
			userid += 1
			userList.append([i[0], i[1], i[2], i[3], i[4]])

		for i in userList:
			if i[1] == inputUsername:
				return "User already exists"
		
		salt = bcrypt.gensalt()
		hashedpw = bcrypt.hashpw(inputPassword.encode('utf-8'), salt)

		cursor.execute("INSERT INTO Users (UserID, UserName, Password, Email, Salt) VALUES (?, ?, ?, ?, ?)", userid, inputUsername, hashedpw, inputEmail, salt)
		cursor.commit()
		return "Account successfully created"

class validateUser(Resource):
	def get(self, username):
		followedSQL = "SELECT UserName FROM Users;"
		cursor = cnxn.cursor()
		cursor.execute(followedSQL)
		followed = cursor.fetchall()
		followedList = []
		for i in followed:
			followedList.append([str(i[0])])
		for i in followedList:
			if i[0] == username:
				return "User exists"
		return "User does not exist"

class followedStocks(Resource):
	def get(self, username):
		followedSQL = "SELECT Symbol, UserID FROM Followed_Stocks;"
		cursor = cnxn.cursor()
		cursor.execute(followedSQL)
		followed = cursor.fetchall()
		followedList = []
		for i in followed:
			followedList.append([str(i[0].upper()), int(i[1])])
		favList = []

		cursor.execute("SELECT UserID, UserName FROM Users;")
		user = cursor.fetchall()
		userList = []
		userid = 0
		for i in user:
			userList.append([i[0], str(i[1])])
			if str(i[1]) == username:
				userid = i[0]


		for i in followedList:
			if i[1] == userid:
				favList.append({"Symbol": i[0], "UserName": username})
			#stockJson.append({"Symbol": i[0], "UserID": i[1]})
			#print(i)
		if favList:
			return favList
		return "User does not have any followed stocks"
	def put(self, username):
		inputSymbol = str(request.args.get('symbol')).upper()

		cursor = cnxn.cursor()
		cursor.execute("SELECT UserID, UserName FROM Users;")
		user = cursor.fetchall()
		userList = []
		userid = 0
		for i in user:
			userList.append([i[0], str(i[1])])
			if str(i[1]) == username:
				userid = i[0]

		cursor = cnxn.cursor()
		cursor.execute("INSERT INTO Followed_Stocks (UserID, Symbol) VALUES (?, ?);", userid, inputSymbol)
		cursor.commit()

		return {"Symbol": inputSymbol, "Username": username}
	def delete(self, username):
		inputSymbol = str(request.args.get('symbol')).upper()

		cursor = cnxn.cursor()
		cursor.execute("SELECT UserID, UserName FROM Users;")
		user = cursor.fetchall()
		userList = []
		userid = 0
		for i in user:
			userList.append([i[0], str(i[1])])
			if str(i[1]) == username:
				userid = i[0]

		cursor = cnxn.cursor()
		cursor.execute("DELETE FROM Followed_Stocks WHERE UserID = ? AND Symbol = ?;", userid, inputSymbol)
		cursor.commit()

		return {"Symbol": inputSymbol, "Username": username}

class stocks(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		nameSQL = "SELECT Name FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(nameSQL)
		name = cursor.fetchall()
		nameList = []
		for i in name:
			nameList.append(str(i))
		nameList = [string.replace("(","") for string in nameList]
		nameList = [string.replace(")","") for string in nameList]
		nameList = [string.replace("'","") for string in nameList]
		nameList = [string.replace(",","") for string in nameList]
		nameList = [string.replace(" ","") for string in nameList]

		sectorSQL = "SELECT Sector FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(sectorSQL)
		sector = cursor.fetchall()
		sectorList = []
		for i in sector:
			sectorList.append(str(i))
		sectorList = [string.replace("(","") for string in sectorList]
		sectorList = [string.replace(")","") for string in sectorList]
		sectorList = [string.replace("'","") for string in sectorList]
		sectorList = [string.replace(",","") for string in sectorList]
		sectorList = [string.replace(" ","") for string in sectorList]

		industrySQL = "SELECT Industry FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(industrySQL)
		industry = cursor.fetchall()
		industryList = []
		for i in industry:
			industryList.append(str(i))
		industryList = [string.replace("(","") for string in industryList]
		industryList = [string.replace(")","") for string in industryList]
		industryList = [string.replace("'","") for string in industryList]
		industryList = [string.replace(",","") for string in industryList]
		industryList = [string.replace(" ","") for string in industryList]

		p2EarningsSQL = "SELECT Price_To_Earnings FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsSQL)
		p2Earnings = cursor.fetchall()
		p2EarningsList = []
		for i in p2Earnings:
			p2EarningsList.append(str(i))
		p2EarningsList = [string.replace("(","") for string in p2EarningsList]
		p2EarningsList = [string.replace(")","") for string in p2EarningsList]
		p2EarningsList = [string.replace("'","") for string in p2EarningsList]
		p2EarningsList = [string.replace(",","") for string in p2EarningsList]
		p2EarningsList = [string.replace(" ","") for string in p2EarningsList]

		p2EarningsGrowthSQL = "SELECT Price_To_Earnings_Growth FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsGrowthSQL)
		p2EarningsGrowth = cursor.fetchall()
		p2EarningsGrowthList = []
		for i in p2EarningsGrowth:
			p2EarningsGrowthList.append(str(i))
		p2EarningsGrowthList = [string.replace("(","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(")","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace("'","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(",","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(" ","") for string in p2EarningsGrowthList]

		p2SalesSQL = "SELECT Price_To_Sales FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2SalesSQL)
		p2Sales = cursor.fetchall()
		p2SalesList = []
		for i in p2Sales:
			p2SalesList.append(str(i))
		p2SalesList = [string.replace("(","") for string in p2SalesList]
		p2SalesList = [string.replace(")","") for string in p2SalesList]
		p2SalesList = [string.replace("'","") for string in p2SalesList]
		p2SalesList = [string.replace(",","") for string in p2SalesList]
		p2SalesList = [string.replace(" ","") for string in p2SalesList]

		p2CashFlowSQL = "SELECT Price_To_Cash_Flow FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2CashFlowSQL)
		p2CashFlow = cursor.fetchall()
		p2CashFlowList = []
		for i in p2CashFlow:
			p2CashFlowList.append(str(i))
		p2CashFlowList = [string.replace("(","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(")","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace("'","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(",","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(" ","") for string in p2CashFlowList]

		p2BookValueSQL = "SELECT Price_To_Book_Value FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2BookValueSQL)
		p2BookValue = cursor.fetchall()
		p2BookValueList = []
		for i in p2BookValue:
			p2BookValueList.append(str(i))
		p2BookValueList = [string.replace("(","") for string in p2BookValueList]
		p2BookValueList = [string.replace(")","") for string in p2BookValueList]
		p2BookValueList = [string.replace("'","") for string in p2BookValueList]
		p2BookValueList = [string.replace(",","") for string in p2BookValueList]
		p2BookValueList = [string.replace(" ","") for string in p2BookValueList]

		d2EquitySQL = "SELECT Debt_To_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(d2EquitySQL)
		d2Equity = cursor.fetchall()
		d2EquityList = []
		for i in d2Equity:
			d2EquityList.append(str(i))
		d2EquityList = [string.replace("(","") for string in d2EquityList]
		d2EquityList = [string.replace(")","") for string in d2EquityList]
		d2EquityList = [string.replace("'","") for string in d2EquityList]
		d2EquityList = [string.replace(",","") for string in d2EquityList]
		d2EquityList = [string.replace(" ","") for string in d2EquityList]

		rOnEquitySQL = "SELECT Return_On_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(rOnEquitySQL)
		rOnEquity = cursor.fetchall()
		rOnEquityList = []
		for i in rOnEquity:
			rOnEquityList.append(str(i))
		rOnEquityList = [string.replace("(","") for string in rOnEquityList]
		rOnEquityList = [string.replace(")","") for string in rOnEquityList]
		rOnEquityList = [string.replace("'","") for string in rOnEquityList]
		rOnEquityList = [string.replace(",","") for string in rOnEquityList]
		rOnEquityList = [string.replace(" ","") for string in rOnEquityList]

		rOnAssetsSQL = "SELECT Return_On_Assets FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(rOnAssetsSQL)
		rOnAssets = cursor.fetchall()
		rOnAssetsList = []
		for i in rOnAssets:
			rOnAssetsList.append(str(i))
		rOnAssetsList = [string.replace("(","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(")","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace("'","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(",","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(" ","") for string in rOnAssetsList]

		profitMarginSQL = "SELECT Profit_Margin FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(profitMarginSQL)
		profitMargin = cursor.fetchall()
		profitMarginList = []
		for i in profitMargin:
			profitMarginList.append(str(i))
		profitMarginList = [string.replace("(","") for string in profitMarginList]
		profitMarginList = [string.replace(")","") for string in profitMarginList]
		profitMarginList = [string.replace("'","") for string in profitMarginList]
		profitMarginList = [string.replace(",","") for string in profitMarginList]
		profitMarginList = [string.replace(" ","") for string in profitMarginList]

		dividendPayoutSQL = "SELECT Dividend_Payout FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendPayoutSQL)
		dividendPayout = cursor.fetchall()
		dividendPayoutList = []
		for i in dividendPayout:
			dividendPayoutList.append(str(i))
		dividendPayoutList = [string.replace("(","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(")","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace("'","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(",","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(" ","") for string in dividendPayoutList]

		currentAssets2LiabilitiesSQL = "SELECT Current_Assets_To_Liabilities FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(currentAssets2LiabilitiesSQL)
		currentAssets2Liabilities = cursor.fetchall()
		currentAssets2LiabilitiesList = []
		for i in currentAssets2Liabilities:
			currentAssets2LiabilitiesList.append(str(i))
		currentAssets2LiabilitiesList = [string.replace("(","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(")","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace("'","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(",","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(" ","") for string in currentAssets2LiabilitiesList]

		quickSQL = "SELECT Quick FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(quickSQL)
		quick = cursor.fetchall()
		quickList = []
		for i in quick:
			quickList.append(str(i))
		quickList = [string.replace("(","") for string in quickList]
		quickList = [string.replace(")","") for string in quickList]
		quickList = [string.replace("'","") for string in quickList]
		quickList = [string.replace(",","") for string in quickList]
		quickList = [string.replace(" ","") for string in quickList]

		interestCoverageSQL = "SELECT Interest_Coverage FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(interestCoverageSQL)
		interestCoverage = cursor.fetchall()
		interestCoverageList = []
		for i in interestCoverage:
			interestCoverageList.append(str(i))
		interestCoverageList = [string.replace("(","") for string in interestCoverageList]
		interestCoverageList = [string.replace(")","") for string in interestCoverageList]
		interestCoverageList = [string.replace("'","") for string in interestCoverageList]
		interestCoverageList = [string.replace(",","") for string in interestCoverageList]
		interestCoverageList = [string.replace(" ","") for string in interestCoverageList]

		assetTurnoverSQL = "SELECT Asset_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(assetTurnoverSQL)
		assetTurnover = cursor.fetchall()
		assetTurnoverList = []
		for i in assetTurnover:
			assetTurnoverList.append(str(i))
		assetTurnoverList = [string.replace("(","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(")","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace("'","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(",","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(" ","") for string in assetTurnoverList]

		inventoryTurnoverSQL = "SELECT Inventory_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(inventoryTurnoverSQL)
		inventoryTurnover = cursor.fetchall()
		inventoryTurnoverList = []
		for i in inventoryTurnover:
			inventoryTurnoverList.append(str(i))
		inventoryTurnoverList = [string.replace("(","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(")","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace("'","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(",","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(" ","") for string in inventoryTurnoverList]

		dividendYieldSQL = "SELECT Dividend_Yield FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendYieldSQL)
		dividendYield = cursor.fetchall()
		dividendYieldList = []
		for i in dividendYield:
			dividendYieldList.append(str(i))
		dividendYieldList = [string.replace("(","") for string in dividendYieldList]
		dividendYieldList = [string.replace(")","") for string in dividendYieldList]
		dividendYieldList = [string.replace("'","") for string in dividendYieldList]
		dividendYieldList = [string.replace(",","") for string in dividendYieldList]
		dividendYieldList = [string.replace(" ","") for string in dividendYieldList]

		stockList = [list(a) for a in zip(symbolList, nameList, sectorList, industryList, p2EarningsList, p2EarningsGrowthList, p2SalesList, p2CashFlowList, p2BookValueList, d2EquityList, rOnEquityList, rOnAssetsList, profitMarginList, dividendPayoutList, currentAssets2LiabilitiesList, quickList, interestCoverageList, assetTurnoverList, inventoryTurnoverList, dividendYieldList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Name": i[1], "Sector": i[2], "Industry": i[3], "Price To Earnings": i[4], "Price To Earnings Growth": i[5], "Price To Sales": i[6], "Price To Cash Flow": i[7], "Price To Book Value": i[8], "Debt To Equity": i[9], "Return On Equity": i[10], "Return On Assets": i[11], "Profit Margin": i[12], "Dividend Payout": i[13], "Current Assets To Liabilities": i[14], "Quick": i[15], "Interest Coverage": i[16], "Asset Turnover": i[17], "Inventory Turnover": i[18], "Dividend Yield": i[19]})
		return stockJson
class stocksIndividual(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		nameSQL = "SELECT Name FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(nameSQL)
		name = cursor.fetchall()
		nameList = []
		for i in name:
			nameList.append(str(i))
		nameList = [string.replace("(","") for string in nameList]
		nameList = [string.replace(")","") for string in nameList]
		nameList = [string.replace("'","") for string in nameList]
		nameList = [string.replace(",","") for string in nameList]
		nameList = [string.replace(" ","") for string in nameList]

		sectorSQL = "SELECT Sector FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(sectorSQL)
		sector = cursor.fetchall()
		sectorList = []
		for i in sector:
			sectorList.append(str(i))
		sectorList = [string.replace("(","") for string in sectorList]
		sectorList = [string.replace(")","") for string in sectorList]
		sectorList = [string.replace("'","") for string in sectorList]
		sectorList = [string.replace(",","") for string in sectorList]
		sectorList = [string.replace(" ","") for string in sectorList]

		industrySQL = "SELECT Industry FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(industrySQL)
		industry = cursor.fetchall()
		industryList = []
		for i in industry:
			industryList.append(str(i))
		industryList = [string.replace("(","") for string in industryList]
		industryList = [string.replace(")","") for string in industryList]
		industryList = [string.replace("'","") for string in industryList]
		industryList = [string.replace(",","") for string in industryList]
		industryList = [string.replace(" ","") for string in industryList]

		p2EarningsSQL = "SELECT Price_To_Earnings FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsSQL)
		p2Earnings = cursor.fetchall()
		p2EarningsList = []
		for i in p2Earnings:
			p2EarningsList.append(str(i))
		p2EarningsList = [string.replace("(","") for string in p2EarningsList]
		p2EarningsList = [string.replace(")","") for string in p2EarningsList]
		p2EarningsList = [string.replace("'","") for string in p2EarningsList]
		p2EarningsList = [string.replace(",","") for string in p2EarningsList]
		p2EarningsList = [string.replace(" ","") for string in p2EarningsList]

		p2EarningsGrowthSQL = "SELECT Price_To_Earnings_Growth FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsGrowthSQL)
		p2EarningsGrowth = cursor.fetchall()
		p2EarningsGrowthList = []
		for i in p2EarningsGrowth:
			p2EarningsGrowthList.append(str(i))
		p2EarningsGrowthList = [string.replace("(","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(")","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace("'","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(",","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(" ","") for string in p2EarningsGrowthList]

		p2SalesSQL = "SELECT Price_To_Sales FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2SalesSQL)
		p2Sales = cursor.fetchall()
		p2SalesList = []
		for i in p2Sales:
			p2SalesList.append(str(i))
		p2SalesList = [string.replace("(","") for string in p2SalesList]
		p2SalesList = [string.replace(")","") for string in p2SalesList]
		p2SalesList = [string.replace("'","") for string in p2SalesList]
		p2SalesList = [string.replace(",","") for string in p2SalesList]
		p2SalesList = [string.replace(" ","") for string in p2SalesList]

		p2CashFlowSQL = "SELECT Price_To_Cash_Flow FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2CashFlowSQL)
		p2CashFlow = cursor.fetchall()
		p2CashFlowList = []
		for i in p2CashFlow:
			p2CashFlowList.append(str(i))
		p2CashFlowList = [string.replace("(","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(")","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace("'","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(",","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(" ","") for string in p2CashFlowList]

		p2BookValueSQL = "SELECT Price_To_Book_Value FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2BookValueSQL)
		p2BookValue = cursor.fetchall()
		p2BookValueList = []
		for i in p2BookValue:
			p2BookValueList.append(str(i))
		p2BookValueList = [string.replace("(","") for string in p2BookValueList]
		p2BookValueList = [string.replace(")","") for string in p2BookValueList]
		p2BookValueList = [string.replace("'","") for string in p2BookValueList]
		p2BookValueList = [string.replace(",","") for string in p2BookValueList]
		p2BookValueList = [string.replace(" ","") for string in p2BookValueList]

		d2EquitySQL = "SELECT Debt_To_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(d2EquitySQL)
		d2Equity = cursor.fetchall()
		d2EquityList = []
		for i in d2Equity:
			d2EquityList.append(str(i))
		d2EquityList = [string.replace("(","") for string in d2EquityList]
		d2EquityList = [string.replace(")","") for string in d2EquityList]
		d2EquityList = [string.replace("'","") for string in d2EquityList]
		d2EquityList = [string.replace(",","") for string in d2EquityList]
		d2EquityList = [string.replace(" ","") for string in d2EquityList]

		rOnEquitySQL = "SELECT Return_On_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(rOnEquitySQL)
		rOnEquity = cursor.fetchall()
		rOnEquityList = []
		for i in rOnEquity:
			rOnEquityList.append(str(i))
		rOnEquityList = [string.replace("(","") for string in rOnEquityList]
		rOnEquityList = [string.replace(")","") for string in rOnEquityList]
		rOnEquityList = [string.replace("'","") for string in rOnEquityList]
		rOnEquityList = [string.replace(",","") for string in rOnEquityList]
		rOnEquityList = [string.replace(" ","") for string in rOnEquityList]

		rOnAssetsSQL = "SELECT Return_On_Assets FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(rOnAssetsSQL)
		rOnAssets = cursor.fetchall()
		rOnAssetsList = []
		for i in rOnAssets:
			rOnAssetsList.append(str(i))
		rOnAssetsList = [string.replace("(","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(")","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace("'","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(",","") for string in rOnAssetsList]
		rOnAssetsList = [string.replace(" ","") for string in rOnAssetsList]

		profitMarginSQL = "SELECT Profit_Margin FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(profitMarginSQL)
		profitMargin = cursor.fetchall()
		profitMarginList = []
		for i in profitMargin:
			profitMarginList.append(str(i))
		profitMarginList = [string.replace("(","") for string in profitMarginList]
		profitMarginList = [string.replace(")","") for string in profitMarginList]
		profitMarginList = [string.replace("'","") for string in profitMarginList]
		profitMarginList = [string.replace(",","") for string in profitMarginList]
		profitMarginList = [string.replace(" ","") for string in profitMarginList]

		dividendPayoutSQL = "SELECT Dividend_Payout FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendPayoutSQL)
		dividendPayout = cursor.fetchall()
		dividendPayoutList = []
		for i in dividendPayout:
			dividendPayoutList.append(str(i))
		dividendPayoutList = [string.replace("(","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(")","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace("'","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(",","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(" ","") for string in dividendPayoutList]

		currentAssets2LiabilitiesSQL = "SELECT Current_Assets_To_Liabilities FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(currentAssets2LiabilitiesSQL)
		currentAssets2Liabilities = cursor.fetchall()
		currentAssets2LiabilitiesList = []
		for i in currentAssets2Liabilities:
			currentAssets2LiabilitiesList.append(str(i))
		currentAssets2LiabilitiesList = [string.replace("(","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(")","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace("'","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(",","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(" ","") for string in currentAssets2LiabilitiesList]

		quickSQL = "SELECT Quick FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(quickSQL)
		quick = cursor.fetchall()
		quickList = []
		for i in quick:
			quickList.append(str(i))
		quickList = [string.replace("(","") for string in quickList]
		quickList = [string.replace(")","") for string in quickList]
		quickList = [string.replace("'","") for string in quickList]
		quickList = [string.replace(",","") for string in quickList]
		quickList = [string.replace(" ","") for string in quickList]

		interestCoverageSQL = "SELECT Interest_Coverage FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(interestCoverageSQL)
		interestCoverage = cursor.fetchall()
		interestCoverageList = []
		for i in interestCoverage:
			interestCoverageList.append(str(i))
		interestCoverageList = [string.replace("(","") for string in interestCoverageList]
		interestCoverageList = [string.replace(")","") for string in interestCoverageList]
		interestCoverageList = [string.replace("'","") for string in interestCoverageList]
		interestCoverageList = [string.replace(",","") for string in interestCoverageList]
		interestCoverageList = [string.replace(" ","") for string in interestCoverageList]

		assetTurnoverSQL = "SELECT Asset_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(assetTurnoverSQL)
		assetTurnover = cursor.fetchall()
		assetTurnoverList = []
		for i in assetTurnover:
			assetTurnoverList.append(str(i))
		assetTurnoverList = [string.replace("(","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(")","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace("'","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(",","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(" ","") for string in assetTurnoverList]

		inventoryTurnoverSQL = "SELECT Inventory_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(inventoryTurnoverSQL)
		inventoryTurnover = cursor.fetchall()
		inventoryTurnoverList = []
		for i in inventoryTurnover:
			inventoryTurnoverList.append(str(i))
		inventoryTurnoverList = [string.replace("(","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(")","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace("'","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(",","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(" ","") for string in inventoryTurnoverList]

		dividendYieldSQL = "SELECT Dividend_Yield FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendYieldSQL)
		dividendYield = cursor.fetchall()
		dividendYieldList = []
		for i in dividendYield:
			dividendYieldList.append(str(i))
		dividendYieldList = [string.replace("(","") for string in dividendYieldList]
		dividendYieldList = [string.replace(")","") for string in dividendYieldList]
		dividendYieldList = [string.replace("'","") for string in dividendYieldList]
		dividendYieldList = [string.replace(",","") for string in dividendYieldList]
		dividendYieldList = [string.replace(" ","") for string in dividendYieldList]

		stockList = [list(a) for a in zip(symbolList, nameList, sectorList, industryList, p2EarningsList, p2EarningsGrowthList, p2SalesList, p2CashFlowList, p2BookValueList, d2EquityList, rOnEquityList, rOnAssetsList, profitMarginList, dividendPayoutList, currentAssets2LiabilitiesList, quickList, interestCoverageList, assetTurnoverList, inventoryTurnoverList, dividendYieldList)]

		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Name": i[1], "Sector": i[2], "Industry": i[3], "Price To Earnings": i[4], "Price To Earnings Growth": i[5], "Price To Sales": i[6], "Price To Cash Flow": i[7], "Price To Book Value": i[8], "Debt To Equity": i[9], "Return On Equity": i[10], "Return On Assets": i[11], "Profit Margin": i[12], "Dividend Payout": i[13], "Current Assets To Liabilities": i[14], "Quick": i[15], "Interest Coverage": i[16], "Asset Turnover": i[17], "Inventory Turnover": i[18], "Dividend Yield": i[19]}

		return "Stock not in database"
	def put(self, stock):
		#Does not update Symbol, Name, Sector or Industry
		#inputSymbol = request.args.get('Symbol')
		inputPriceToEarnings = str(request.args.get('pricetoearnings'))
		inputPriceToEarningsGrowth = str(request.args.get('pricetoearningsgrowth'))
		inputPriceToSales = str(request.args.get('pricetosales'))
		inputPriceToCashFlow = str(request.args.get('pricetocashflow'))
		inputPriceToBookValue = str(request.args.get('pricetobookvalue'))
		inputDebtToEquity = str(request.args.get('debttoequity'))
		inputReturnOnEquity = str(request.args.get('returnonequity'))
		inputReturnOnAssets = str(request.args.get('returnonassets'))
		inputProfitMargin = str(request.args.get('profitmargin'))
		inputDividendPayout = str(request.args.get('dividendpayout'))
		inputCurrentAssetsToLiabilities = str(request.args.get('currentassetstoliabilities'))
		inputQuick = str(request.args.get('quick'))
		inputInterestCoverage = str(request.args.get('interestCoverage'))
		inputAssetTurnover = str(request.args.get('assetturnover'))
		inputInventoryTurnover = str(request.args.get('inventoryturnover'))
		inputDividendYield = str(request.args.get('dividendyield'))
		if inputPriceToEarnings == "":
			inputPriceToEarnings = None
		if inputPriceToEarningsGrowth == "":
			inputPriceToEarningsGrowth = None
		if inputPriceToSales == "":
			inputPriceToSales = None
		if inputPriceToCashFlow == "":
			inputPriceToCashFlow = None
		if inputPriceToBookValue == "":
			inputPriceToBookValue = None
		if inputDebtToEquity == "":
			inputDebtToEquity = None
		if inputReturnOnEquity == "":
			inputReturnOnEquity = None
		if inputReturnOnAssets == "":
			inputReturnOnAssets = None
		if inputProfitMargin == "":
			inputProfitMargin = None
		if inputDividendPayout == "":
			inputDividendPayout = None
		if inputCurrentAssetsToLiabilities == "":
			inputCurrentAssetsToLiabilities = None
		if inputQuick == "":
			inputQuick = None
		if inputInterestCoverage == "":
			inputInterestCoverage = None
		if inputAssetTurnover == "":
			inputAssetTurnover = None
		if inputInventoryTurnover == "":
			inputInventoryTurnover = None
		if inputDividendYield == "":
			inputDividendYield = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		nameSQL = "SELECT Name FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(nameSQL)
		name = cursor.fetchall()
		nameList = []
		for i in name:
			nameList.append(str(i))
		nameList = [string.replace("(","") for string in nameList]
		nameList = [string.replace(")","") for string in nameList]
		nameList = [string.replace("'","") for string in nameList]
		nameList = [string.replace(",","") for string in nameList]
		nameList = [string.replace(" ","") for string in nameList]

		sectorSQL = "SELECT Sector FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(sectorSQL)
		sector = cursor.fetchall()
		sectorList = []
		for i in sector:
			sectorList.append(str(i))
		sectorList = [string.replace("(","") for string in sectorList]
		sectorList = [string.replace(")","") for string in sectorList]
		sectorList = [string.replace("'","") for string in sectorList]
		sectorList = [string.replace(",","") for string in sectorList]
		sectorList = [string.replace(" ","") for string in sectorList]

		industrySQL = "SELECT Industry FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(industrySQL)
		industry = cursor.fetchall()
		industryList = []
		for i in industry:
			industryList.append(str(i))
		industryList = [string.replace("(","") for string in industryList]
		industryList = [string.replace(")","") for string in industryList]
		industryList = [string.replace("'","") for string in industryList]
		industryList = [string.replace(",","") for string in industryList]
		industryList = [string.replace(" ","") for string in industryList]		

		stockList = []
		stockList = [list(a) for a in zip(symbolList, nameList, sectorList, industryList)]


		for i in stockList:
			if i[0] == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Earnings = ? WHERE Symbol = ?", inputPriceToEarnings, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Price_To_Earnings_Growth = ? WHERE Symbol = ?", inputPriceToEarningsGrowth, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Price_To_Sales = ? WHERE Symbol = ?", inputPriceToSales, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Price_To_Cash_Flow = ? WHERE Symbol = ?", inputPriceToCashFlow, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Price_To_BookValue = ? WHERE Symbol = ?", inputPriceToBookValue, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Debt_To_Equity = ? WHERE Symbol = ?", inputDebtToEquity, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Return_On_Equity = ? WHERE Symbol = ?", inputReturnOnEquity, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Return_On_Assets = ? WHERE Symbol = ?", inputReturnOnAssets, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Profit_Margin = ? WHERE Symbol = ?", inputProfitMargin, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Dividend_Payout = ? WHERE Symbol = ?", inputDividendPayout, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Current_Assets_To_Liabilities = ? WHERE Symbol = ?", inputCurrentAssetsToLiabilities, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Quick = ? WHERE Symbol = ?", inputQuick, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Interest_Coverage = ? WHERE Symbol = ?", inputInterestCoverage, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Asset_Turnover = ? WHERE Symbol = ?", inputAssetTurnover, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Inventory_Turnover = ? WHERE Symbol = ?", inputinventoryTurnover, stock.upper())
				cursor.commit()
				cursor.execute("UPDATE Stock_Info SET Dividend_Yield = ? WHERE Symbol = ?", inputDividendYield, stock.upper())
				cursor.commit()

				return {"Symbol": stock.upper(), "Name": i[1], "Sector": i[2], "Industry": i[3], "Price To Earnings": inputPriceToEarnings, "Price To Earnings Growth": inputPriceToEarningsGrowth, "Price To Sales": inputPriceToSales, "Price To Cash Flow": inputPriceToCashFlow, "Price To Book Value": inputPriceToBookValue, "Debt To Equity": inputDebtToEquity, "Return On Equity": inputReturnOnEquity, "Return On Assets": inputReturnOnAssets, "Profit Margin": inputProfitMargin, "Dividend Payout": inputDividendPayout, "Current Assets To Liabilities": inputCurrentAssetsToLiabilities, "Quick": inputQuick, "Interest Coverage": inputInterestCoverage, "Asset Turnover": inputAssetTurnover, "Inventory Turnover": inputInventoryTurnover, "Dividend Yield": inputDividendYield}

		#stockList.append([stock.upper(), inputinventoryTurnover])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputinventoryTurnover}
		return "Stock does not exist in database"
class stockSymbol(Resource):
	def get(self):
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for sym in symbol:
			symbolList.append(str(sym))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]
		symbolJson=[]
		for symbols in symbolList:
			symbolJson.append({"Symbol": symbols})

		return symbolJson
class stockIndividualSymbol(Resource):
	def get(self, stock):
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for sym in symbol:
			symbolList.append(str(sym))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]
		for symbols in symbolList:
			if symbols == stock.upper():
				return {"Symbol": symbols}

		return "Stock does not exist in database"
class stockName(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		nameSQL = "SELECT Name FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(nameSQL)
		name = cursor.fetchall()
		nameList = []
		for sym in name:
			nameList.append(str(sym))
		nameList = [string.replace("(","") for string in nameList]
		nameList = [string.replace(")","") for string in nameList]
		nameList = [string.replace("'","") for string in nameList]
		nameList = [string.replace(",","") for string in nameList]
		nameList = [string.replace(" ","") for string in nameList]

		stockList = [list(a) for a in zip(symbolList, nameList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Name": i[1]})
		return stockJson
class stockIndividualName(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		nameSQL = "SELECT Name FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(nameSQL)
		name = cursor.fetchall()
		nameList = []
		for sym in name:
			nameList.append(str(sym))
		nameList = [string.replace("(","") for string in nameList]
		nameList = [string.replace(")","") for string in nameList]
		nameList = [string.replace("'","") for string in nameList]
		nameList = [string.replace(",","") for string in nameList]
		nameList = [string.replace(" ","") for string in nameList]

		stockList = [list(a) for a in zip(symbolList, nameList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Name": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputName = str(request.args.get('name'))
		if inputName == "":
			inputName = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Name = ? WHERE Symbol = ?", inputName, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Name": str(inputName)}

		#stockList.append([stock.upper(), inputName])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputName}
		return "Stock does not exist in database"
class stockPriceToEarnings(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2EarningsSQL = "SELECT Price_To_Earnings FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsSQL)
		p2Earnings = cursor.fetchall()
		p2EarningsList = []
		for i in p2Earnings:
			p2EarningsList.append(str(i))
		p2EarningsList = [string.replace("(","") for string in p2EarningsList]
		p2EarningsList = [string.replace(")","") for string in p2EarningsList]
		p2EarningsList = [string.replace("'","") for string in p2EarningsList]
		p2EarningsList = [string.replace(",","") for string in p2EarningsList]
		p2EarningsList = [string.replace(" ","") for string in p2EarningsList]

		stockList = [list(a) for a in zip(symbolList, p2EarningsList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Price To Earnings": i[1]})
		return stockJson
class stockIndividualPriceToEarnings(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2EarningsSQL = "SELECT Price_To_Earnings FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsSQL)
		p2Earnings = cursor.fetchall()
		p2EarningsList = []
		for i in p2Earnings:
			p2EarningsList.append(str(i))
		p2EarningsList = [string.replace("(","") for string in p2EarningsList]
		p2EarningsList = [string.replace(")","") for string in p2EarningsList]
		p2EarningsList = [string.replace("'","") for string in p2EarningsList]
		p2EarningsList = [string.replace(",","") for string in p2EarningsList]
		p2EarningsList = [string.replace(" ","") for string in p2EarningsList]

		stockList = [list(a) for a in zip(symbolList, p2EarningsList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Price To Earnings": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol')
		inputPriceToEarnings = str(request.args.get('pricetoearnings'))
		if inputPriceToEarnings == "":
			inputPriceToEarnings = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Earnings = ? WHERE Symbol = ?", inputPriceToEarnings, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Price To Earnings": str(inputPriceToEarnings)}

		#stockList.append([stock.upper(), inputPriceToEarnings])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputPriceToEarnings}
		return "Stock does not exist in database"
class stockPriceToEarningsGrowth(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2EarningsGrowthSQL = "SELECT Price_To_Earnings_Growth FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsGrowthSQL)
		p2EarningsGrowth = cursor.fetchall()
		p2EarningsGrowthList = []
		for i in p2EarningsGrowth:
			p2EarningsGrowthList.append(str(i))
		p2EarningsGrowthList = [string.replace("(","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(")","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace("'","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(",","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(" ","") for string in p2EarningsGrowthList]

		stockList = [list(a) for a in zip(symbolList, p2EarningsGrowthList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Price To Earnings": i[1]})
		return stockJson
class stockIndividualPriceToEarningsGrowth(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2EarningsGrowthSQL = "SELECT Price_To_Earnings FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2EarningsGrowthSQL)
		p2EarningsGrowth = cursor.fetchall()
		p2EarningsGrowthList = []
		for i in p2EarningsGrowth:
			p2EarningsGrowthList.append(str(i))
		p2EarningsGrowthList = [string.replace("(","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(")","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace("'","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(",","") for string in p2EarningsGrowthList]
		p2EarningsGrowthList = [string.replace(" ","") for string in p2EarningsGrowthList]

		stockList = [list(a) for a in zip(symbolList, p2EarningsGrowthList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Price To Earnings": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputPriceToEarningsGrowth = str(request.args.get('pricetoearningsgrowth'))
		if inputPriceToEarningsGrowth == "":
			inputPriceToEarningsGrowth = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Earnings_Growth = ? WHERE Symbol = ?", inputPriceToEarningsGrowth, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Price To Earnings Growth": str(inputPriceToEarningsGrowth)}

		#stockList.append([stock.upper(), inputPriceToEarningsGrowth])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputPriceToEarningsGrowth}
		return "Stock does not exist in database"
class stockPriceToSales(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2SalesSQL = "SELECT Price_To_Sales FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2SalesSQL)
		p2Sales = cursor.fetchall()
		p2SalesList = []
		for i in p2Sales:
			p2SalesList.append(str(i))
		p2SalesList = [string.replace("(","") for string in p2SalesList]
		p2SalesList = [string.replace(")","") for string in p2SalesList]
		p2SalesList = [string.replace("'","") for string in p2SalesList]
		p2SalesList = [string.replace(",","") for string in p2SalesList]
		p2SalesList = [string.replace(" ","") for string in p2SalesList]

		stockList = [list(a) for a in zip(symbolList, p2SalesList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Price To Sales": i[1]})
		return stockJson
class stockIndividualPriceToSales(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2SalesSQL = "SELECT Price_To_Sales FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2SalesSQL)
		p2Sales = cursor.fetchall()
		p2SalesList = []
		for i in p2Sales:
			p2SalesList.append(str(i))
		p2SalesList = [string.replace("(","") for string in p2SalesList]
		p2SalesList = [string.replace(")","") for string in p2SalesList]
		p2SalesList = [string.replace("'","") for string in p2SalesList]
		p2SalesList = [string.replace(",","") for string in p2SalesList]
		p2SalesList = [string.replace(" ","") for string in p2SalesList]

		stockList = [list(a) for a in zip(symbolList, p2SalesList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Price To Sales": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputPriceToSales = str(request.args.get('pricetosales'))
		if inputPriceToSales == "":
			inputPriceToSales = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Sales = ? WHERE Symbol = ?", inputPriceToSales, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Price To Sales": str(inputPriceToSales)}

		#stockList.append([stock.upper(), inputPriceToSales])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputPriceToSales}
		return "Stock does not exist in database"
class stockPriceToCashFlow(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2CashFlowSQL = "SELECT Price_To_Cash_Flow FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2CashFlowSQL)
		p2CashFlow = cursor.fetchall()
		p2CashFlowList = []
		for i in p2CashFlow:
			p2CashFlowList.append(str(i))
		p2CashFlowList = [string.replace("(","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(")","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace("'","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(",","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(" ","") for string in p2CashFlowList]

		stockList = [list(a) for a in zip(symbolList, p2CashFlowList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Price To Cash Flow": i[1]})
		return stockJson		
class stockIndividualPriceToCashFlow(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2CashFlowSQL = "SELECT Price_To_Cash_Flow FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2CashFlowSQL)
		p2CashFlow = cursor.fetchall()
		p2CashFlowList = []
		for i in p2CashFlow:
			p2CashFlowList.append(str(i))
		p2CashFlowList = [string.replace("(","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(")","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace("'","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(",","") for string in p2CashFlowList]
		p2CashFlowList = [string.replace(" ","") for string in p2CashFlowList]

		stockList = [list(a) for a in zip(symbolList, p2CashFlowList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Price To Cash Flow": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputPriceToCashFlow = str(request.args.get('pricetocashflow'))
		if inputPriceToCashFlow == "":
			inputPriceToCashFlow = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Cash_Flow = ? WHERE Symbol = ?", inputPriceToCashFlow, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Price To Cash Flow": str(inputPriceToCashFlow)}

		#stockList.append([stock.upper(), inputPriceToCashFlow])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputPriceToCashFlow}
		return "Stock does not exist in database"
class stockPriceToBookValue(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2BookValueSQL = "SELECT Price_To_Book_Value FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2BookValueSQL)
		p2BookValue = cursor.fetchall()
		p2BookValueList = []
		for i in p2BookValue:
			p2BookValueList.append(str(i))
		p2BookValueList = [string.replace("(","") for string in p2BookValueList]
		p2BookValueList = [string.replace(")","") for string in p2BookValueList]
		p2BookValueList = [string.replace("'","") for string in p2BookValueList]
		p2BookValueList = [string.replace(",","") for string in p2BookValueList]
		p2BookValueList = [string.replace(" ","") for string in p2BookValueList]

		stockList = [list(a) for a in zip(symbolList, p2BookValueList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Price To Book Value": i[1]})
		return stockJson
class stockIndividualPriceToBookValue(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		p2BookValueSQL = "SELECT Price_To_Book_Value FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(p2BookValueSQL)
		p2BookValue = cursor.fetchall()
		p2BookValueList = []
		for i in p2BookValue:
			p2BookValueList.append(str(i))
		p2BookValueList = [string.replace("(","") for string in p2BookValueList]
		p2BookValueList = [string.replace(")","") for string in p2BookValueList]
		p2BookValueList = [string.replace("'","") for string in p2BookValueList]
		p2BookValueList = [string.replace(",","") for string in p2BookValueList]
		p2BookValueList = [string.replace(" ","") for string in p2BookValueList]

		stockList = [list(a) for a in zip(symbolList, p2BookValueList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Price To Book Value": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputPriceToBookValue = str(request.args.get('pricetobookvalue'))
		if inputPriceToBookValue == "":
			inputPriceToBookValue = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Price_To_Book_Value = ? WHERE Symbol = ?", inputPriceToBookValue, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Price To Book Value": str(inputPriceToBookValue)}

		#stockList.append([stock.upper(), inputPriceToBookValue])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputPriceToBookValue}
		return "Stock does not exist in database"
class stockDebtToEquity(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		d2EquitySQL = "SELECT Debt_To_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(d2EquitySQL)
		d2Equity = cursor.fetchall()
		d2EquityList = []
		for i in d2Equity:
			d2EquityList.append(str(i))
		d2EquityList = [string.replace("(","") for string in d2EquityList]
		d2EquityList = [string.replace(")","") for string in d2EquityList]
		d2EquityList = [string.replace("'","") for string in d2EquityList]
		d2EquityList = [string.replace(",","") for string in d2EquityList]
		d2EquityList = [string.replace(" ","") for string in d2EquityList]

		stockList = [list(a) for a in zip(symbolList, d2EquityList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Debt To Equity": i[1]})
		return stockJson
class stockIndividualDebtToEquity(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		d2EquitySQL = "SELECT Debt_To_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(d2EquitySQL)
		d2Equity = cursor.fetchall()
		d2EquityList = []
		for i in d2Equity:
			d2EquityList.append(str(i))
		d2EquityList = [string.replace("(","") for string in d2EquityList]
		d2EquityList = [string.replace(")","") for string in d2EquityList]
		d2EquityList = [string.replace("'","") for string in d2EquityList]
		d2EquityList = [string.replace(",","") for string in d2EquityList]
		d2EquityList = [string.replace(" ","") for string in d2EquityList]

		stockList = [list(a) for a in zip(symbolList, d2EquityList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Debt To Equity": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputDebtToEquity = str(request.args.get('debttoequity'))
		if inputDebtToEquity == "":
			inputDebtToEquity = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Debt_To_Equity = ? WHERE Symbol = ?", inputDebtToEquity, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Debt To Equity": str(inputDebtToEquity)}

		#stockList.append([stock.upper(), inputDebtToEquity])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputDebtToEquity}
		return "Stock does not exist in database"
class stockReturnOnEquity(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		returnOnEquitySQL = "SELECT Return_On_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(returnOnEquitySQL)
		returnOnEquity = cursor.fetchall()
		returnOnEquityList = []
		for i in returnOnEquity:
			returnOnEquityList.append(str(i))
		returnOnEquityList = [string.replace("(","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(")","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace("'","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(",","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(" ","") for string in returnOnEquityList]

		stockList = [list(a) for a in zip(symbolList, returnOnEquityList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Return On Equity": i[1]})
		return stockJson
class stockIndividualReturnOnEquity(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		returnOnEquitySQL = "SELECT Return_On_Equity FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(returnOnEquitySQL)
		returnOnEquity = cursor.fetchall()
		returnOnEquityList = []
		for i in returnOnEquity:
			returnOnEquityList.append(str(i))
		returnOnEquityList = [string.replace("(","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(")","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace("'","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(",","") for string in returnOnEquityList]
		returnOnEquityList = [string.replace(" ","") for string in returnOnEquityList]

		stockList = [list(a) for a in zip(symbolList, returnOnEquityList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Return On Equity": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputReturnOnEquity = str(request.args.get('returnonequity'))
		if inputReturnOnEquity == "":
			inputReturnOnEquity = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Return_On_Equity = ? WHERE Symbol = ?", inputReturnOnEquity, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Return On Equity": str(inputReturnOnEquity)}

		#stockList.append([stock.upper(), inputReturnOnEquity])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputReturnOnEquity}
		return "Stock does not exist in database"
class stockReturnOnAssets(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		returnOnAssetsSQL = "SELECT Return_On_Assets FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(returnOnAssetsSQL)
		returnOnAssets = cursor.fetchall()
		returnOnAssetsList = []
		for i in returnOnAssets:
			returnOnAssetsList.append(str(i))
		returnOnAssetsList = [string.replace("(","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(")","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace("'","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(",","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(" ","") for string in returnOnAssetsList]

		stockList = [list(a) for a in zip(symbolList, returnOnAssetsList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Return On Assets": i[1]})
		return stockJson
class stockIndividualReturnOnAssets(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		returnOnAssetsSQL = "SELECT Return_On_Assets FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(returnOnAssetsSQL)
		returnOnAssets = cursor.fetchall()
		returnOnAssetsList = []
		for i in returnOnAssets:
			returnOnAssetsList.append(str(i))
		returnOnAssetsList = [string.replace("(","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(")","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace("'","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(",","") for string in returnOnAssetsList]
		returnOnAssetsList = [string.replace(" ","") for string in returnOnAssetsList]

		stockList = [list(a) for a in zip(symbolList, returnOnAssetsList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Return On Assets": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputReturnOnAssets = str(request.args.get('returnonassets'))
		if inputReturnOnAssets == "":
			inputReturnOnAssets = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Return_On_Assets = ? WHERE Symbol = ?", inputReturnOnAssets, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Return On Assets": str(inputReturnOnAssets)}

		#stockList.append([stock.upper(), inputReturnOnAssets])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputReturnOnAssets}
		return "Stock does not exist in database"
class stockProfitMargin(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		profitMarginSQL = "SELECT Profit_Margin FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(profitMarginSQL)
		profitMargin = cursor.fetchall()
		profitMarginList = []
		for i in profitMargin:
			profitMarginList.append(str(i))
		profitMarginList = [string.replace("(","") for string in profitMarginList]
		profitMarginList = [string.replace(")","") for string in profitMarginList]
		profitMarginList = [string.replace("'","") for string in profitMarginList]
		profitMarginList = [string.replace(",","") for string in profitMarginList]
		profitMarginList = [string.replace(" ","") for string in profitMarginList]

		stockList = [list(a) for a in zip(symbolList, profitMarginList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Profit Margin": i[1]})
		return stockJson
class stockIndividualProfitMargin(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		profitMarginSQL = "SELECT Profit_Margin FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(profitMarginSQL)
		profitMargin = cursor.fetchall()
		profitMarginList = []
		for i in profitMargin:
			profitMarginList.append(str(i))
		profitMarginList = [string.replace("(","") for string in profitMarginList]
		profitMarginList = [string.replace(")","") for string in profitMarginList]
		profitMarginList = [string.replace("'","") for string in profitMarginList]
		profitMarginList = [string.replace(",","") for string in profitMarginList]
		profitMarginList = [string.replace(" ","") for string in profitMarginList]

		stockList = [list(a) for a in zip(symbolList, profitMarginList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Profit Margin": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputProfitMargin = str(request.args.get('profitmargin'))
		if inputProfitMargin == "":
			inputProfitMargin = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Profit_Margin = ? WHERE Symbol = ?", inputProfitMargin, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Profit Margin": str(inputProfitMargin)}

		#stockList.append([stock.upper(), inputProfitMargin])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputProfitMargin}
		return "Stock does not exist in database"
class stockDividendPayout(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		dividendPayoutSQL = "SELECT Dividend_Payout FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendPayoutSQL)
		dividendPayout = cursor.fetchall()
		dividendPayoutList = []
		for i in dividendPayout:
			dividendPayoutList.append(str(i))
		dividendPayoutList = [string.replace("(","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(")","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace("'","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(",","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(" ","") for string in dividendPayoutList]

		stockList = [list(a) for a in zip(symbolList, dividendPayoutList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Dividend Payout": i[1]})
		return stockJson
class stockIndividualDividendPayout(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		dividendPayoutSQL = "SELECT Dividend_Payout FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendPayoutSQL)
		dividendPayout = cursor.fetchall()
		dividendPayoutList = []
		for i in dividendPayout:
			dividendPayoutList.append(str(i))
		dividendPayoutList = [string.replace("(","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(")","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace("'","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(",","") for string in dividendPayoutList]
		dividendPayoutList = [string.replace(" ","") for string in dividendPayoutList]

		stockList = [list(a) for a in zip(symbolList, dividendPayoutList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Dividend Payout": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputDividendPayout = str(request.args.get('dividendpayout'))
		if inputDividendPayout == "":
			inputDividendPayout = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Dividend_Payout = ? WHERE Symbol = ?", inputDividendPayout, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Dividend Payout": str(inputDividendPayout)}

		#stockList.append([stock.upper(), inputDividendPayout])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputDividendPayout}
		return "Stock does not exist in database"
class stockCurrentAssetsToLiabilities(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		currentAssets2LiabilitiesSQL = "SELECT Current_Assets_To_Liabilities FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(currentAssets2LiabilitiesSQL)
		currentAssets2Liabilities = cursor.fetchall()
		currentAssets2LiabilitiesList = []
		for i in currentAssets2Liabilities:
			currentAssets2LiabilitiesList.append(str(i))
		currentAssets2LiabilitiesList = [string.replace("(","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(")","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace("'","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(",","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(" ","") for string in currentAssets2LiabilitiesList]

		stockList = [list(a) for a in zip(symbolList, currentAssets2LiabilitiesList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Current Assets To Liabilities": i[1]})
		return stockJson
class stockIndividualCurrentAssetsToLiabilities(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		currentAssets2LiabilitiesSQL = "SELECT Current_Assets_To_Liabilities FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(currentAssets2LiabilitiesSQL)
		currentAssets2Liabilities = cursor.fetchall()
		currentAssets2LiabilitiesList = []
		for i in currentAssets2Liabilities:
			currentAssets2LiabilitiesList.append(str(i))
		currentAssets2LiabilitiesList = [string.replace("(","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(")","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace("'","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(",","") for string in currentAssets2LiabilitiesList]
		currentAssets2LiabilitiesList = [string.replace(" ","") for string in currentAssets2LiabilitiesList]

		stockList = [list(a) for a in zip(symbolList, currentAssets2LiabilitiesList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Current_Assets_To_Liabilities": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputCurrentAssetsToLiabilities = str(request.args.get('currentassetstoliabilities'))
		if inputCurrentAssetsToLiabilities == "":
			inputCurrentAssetsToLiabilities = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Current_Assets_To_Liabilities = ? WHERE Symbol = ?", inputCurrentAssetsToLiabilities, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Current Assets To Liabilities": str(inputCurrentAssetsToLiabilities)}

		#stockList.append([stock.upper(), inputCurrentAssetsToLiabilities])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputCurrentAssetsToLiabilities}
		return "Stock does not exist in database"
class stockQuick(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		quickSQL = "SELECT Quick FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(quickSQL)
		quick = cursor.fetchall()
		quickList = []
		for i in quick:
			quickList.append(str(i))
		quickList = [string.replace("(","") for string in quickList]
		quickList = [string.replace(")","") for string in quickList]
		quickList = [string.replace("'","") for string in quickList]
		quickList = [string.replace(",","") for string in quickList]
		quickList = [string.replace(" ","") for string in quickList]

		stockList = [list(a) for a in zip(symbolList, quickList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Quick": i[1]})
		return stockJson
class stockIndividualQuick(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		quickSQL = "SELECT Quick FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(quickSQL)
		quick = cursor.fetchall()
		quickList = []
		for i in quick:
			quickList.append(str(i))
		quickList = [string.replace("(","") for string in quickList]
		quickList = [string.replace(")","") for string in quickList]
		quickList = [string.replace("'","") for string in quickList]
		quickList = [string.replace(",","") for string in quickList]
		quickList = [string.replace(" ","") for string in quickList]

		stockList = [list(a) for a in zip(symbolList, quickList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Quick": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputQuick = str(request.args.get('quick'))
		if inputQuick == "":
			inputQuick = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Quick = ? WHERE Symbol = ?", inputQuick, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Quick": str(inputQuick)}

		#stockList.append([stock.upper(), inputQuick])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputQuick}
		return "Stock does not exist in database"
class stockInterestCoverage(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		interestCoverageSQL = "SELECT Interest_Coverage FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(interestCoverageSQL)
		interestCoverage = cursor.fetchall()
		interestCoverageList = []
		for i in interestCoverage:
			interestCoverageList.append(str(i))
		interestCoverageList = [string.replace("(","") for string in interestCoverageList]
		interestCoverageList = [string.replace(")","") for string in interestCoverageList]
		interestCoverageList = [string.replace("'","") for string in interestCoverageList]
		interestCoverageList = [string.replace(",","") for string in interestCoverageList]
		interestCoverageList = [string.replace(" ","") for string in interestCoverageList]

		stockList = [list(a) for a in zip(symbolList, interestCoverageList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Interest Coverage": i[1]})
		return stockJson
class stockIndividualInterestCoverage(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		interestCoverageSQL = "SELECT Interest_Coverage FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(interestCoverageSQL)
		interestCoverage = cursor.fetchall()
		interestCoverageList = []
		for i in interestCoverage:
			interestCoverageList.append(str(i))
		interestCoverageList = [string.replace("(","") for string in interestCoverageList]
		interestCoverageList = [string.replace(")","") for string in interestCoverageList]
		interestCoverageList = [string.replace("'","") for string in interestCoverageList]
		interestCoverageList = [string.replace(",","") for string in interestCoverageList]
		interestCoverageList = [string.replace(" ","") for string in interestCoverageList]

		stockList = [list(a) for a in zip(symbolList, interestCoverageList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Interest Coverage": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputinterestCoverage = str(request.args.get('interestCoverage'))
		if inputinterestCoverage == "":
			inputinterestCoverage = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Interest_Coverage = ? WHERE Symbol = ?", inputinterestCoverage, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Interest Coverage": str(inputinterestCoverage)}

		#stockList.append([stock.upper(), inputinterestCoverage])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputinterestCoverage}
		return "Stock does not exist in database"
class stockAssetTurnover(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		assetTurnoverSQL = "SELECT Asset_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(assetTurnoverSQL)
		assetTurnover = cursor.fetchall()
		assetTurnoverList = []
		for i in assetTurnover:
			assetTurnoverList.append(str(i))
		assetTurnoverList = [string.replace("(","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(")","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace("'","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(",","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(" ","") for string in assetTurnoverList]

		stockList = [list(a) for a in zip(symbolList, assetTurnoverList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Asset Turnover": i[1]})
		return stockJson
class stockIndividualAssetTurnover(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		assetTurnoverSQL = "SELECT Asset_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(assetTurnoverSQL)
		assetTurnover = cursor.fetchall()
		assetTurnoverList = []
		for i in assetTurnover:
			assetTurnoverList.append(str(i))
		assetTurnoverList = [string.replace("(","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(")","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace("'","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(",","") for string in assetTurnoverList]
		assetTurnoverList = [string.replace(" ","") for string in assetTurnoverList]

		stockList = [list(a) for a in zip(symbolList, assetTurnoverList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Asset Turnover": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputassetTurnover = str(request.args.get('assetturnover'))
		if inputassetTurnover == "":
			inputassetTurnover = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Asset_Turnover = ? WHERE Symbol = ?", inputassetTurnover, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Asset Turnover": str(inputassetTurnover)}

		#stockList.append([stock.upper(), inputassetTurnover])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputassetTurnover}
		return "Stock does not exist in database"	
class stockInventoryTurnover(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		inventoryTurnoverSQL = "SELECT Inventory_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(inventoryTurnoverSQL)
		inventoryTurnover = cursor.fetchall()
		inventoryTurnoverList = []
		for i in inventoryTurnover:
			inventoryTurnoverList.append(str(i))
		inventoryTurnoverList = [string.replace("(","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(")","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace("'","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(",","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(" ","") for string in inventoryTurnoverList]

		stockList = [list(a) for a in zip(symbolList, inventoryTurnoverList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Inventory Turnover": i[1]})
		return stockJson
class stockIndividualInventoryTurnover(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		inventoryTurnoverSQL = "SELECT Inventory_Turnover FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(inventoryTurnoverSQL)
		inventoryTurnover = cursor.fetchall()
		inventoryTurnoverList = []
		for i in inventoryTurnover:
			inventoryTurnoverList.append(str(i))
		inventoryTurnoverList = [string.replace("(","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(")","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace("'","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(",","") for string in inventoryTurnoverList]
		inventoryTurnoverList = [string.replace(" ","") for string in inventoryTurnoverList]

		stockList = [list(a) for a in zip(symbolList, inventoryTurnoverList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Inventory Turnover": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputinventoryTurnover = str(request.args.get('inventoryturnover'))
		if inputinventoryTurnover == "":
			inputinventoryTurnover = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Inventory_Turnover = ? WHERE Symbol = ?", inputinventoryTurnover, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Inventory Turnover": str(inputinventoryTurnover)}

		#stockList.append([stock.upper(), inputinventoryTurnover])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputinventoryTurnover}
		return "Stock does not exist in database"
class stockDividendYield(Resource):
	def get(self):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		dividendYieldSQL = "SELECT Dividend_Yield FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendYieldSQL)
		dividendYield = cursor.fetchall()
		dividendYieldList = []
		for i in dividendYield:
			dividendYieldList.append(str(i))
		dividendYieldList = [string.replace("(","") for string in dividendYieldList]
		dividendYieldList = [string.replace(")","") for string in dividendYieldList]
		dividendYieldList = [string.replace("'","") for string in dividendYieldList]
		dividendYieldList = [string.replace(",","") for string in dividendYieldList]
		dividendYieldList = [string.replace(" ","") for string in dividendYieldList]

		stockList = [list(a) for a in zip(symbolList, dividendYieldList)]
		stockJson = []
		for i in stockList:
			stockJson.append({"Symbol": i[0], "Dividend Yield": i[1]})
		return stockJson
class stockIndividualDividendYield(Resource):
	def get(self, stock):
		stockList = []
		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		dividendYieldSQL = "SELECT Dividend_Yield FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(dividendYieldSQL)
		dividendYield = cursor.fetchall()
		dividendYieldList = []
		for i in dividendYield:
			dividendYieldList.append(str(i))
		dividendYieldList = [string.replace("(","") for string in dividendYieldList]
		dividendYieldList = [string.replace(")","") for string in dividendYieldList]
		dividendYieldList = [string.replace("'","") for string in dividendYieldList]
		dividendYieldList = [string.replace(",","") for string in dividendYieldList]
		dividendYieldList = [string.replace(" ","") for string in dividendYieldList]

		stockList = [list(a) for a in zip(symbolList, dividendYieldList)]
		for i in stockList:
			if i[0] == stock.upper():
				return {"Symbol": i[0], "Dividend Yield": i[1]}

		return "Stock does not exist in database"
	def put(self, stock):
		#inputSymbol = request.args.get('Symbol']
		inputDividendYield = str(request.args.get('dividendyield'))
		if inputDividendYield == "":
			inputDividendYield = None

		symbolSQL = "SELECT Symbol FROM Stock_Info;"
		cursor = cnxn.cursor()
		cursor.execute(symbolSQL)
		symbol = cursor.fetchall()
		symbolList = []
		for i in symbol:
			symbolList.append(str(i))
		symbolList = [string.replace("(","") for string in symbolList]
		symbolList = [string.replace(")","") for string in symbolList]
		symbolList = [string.replace("'","") for string in symbolList]
		symbolList = [string.replace(",","") for string in symbolList]
		symbolList = [string.replace(" ","") for string in symbolList]

		for i in symbolList:
			if i == stock.upper():
				cursor.execute("UPDATE Stock_Info SET Dividend_Yield = ? WHERE Symbol = ?", inputDividendYield, stock.upper())
				cursor.commit()
				return {"Symbol": stock.upper(), "Dividend Yield": str(inputDividendYield)}

		#stockList.append([stock.upper(), inputDividendYield])
		#exeSQL = "INSERT INTO Stock_Info (Symbol, Name, Sector, Industry, Price_To_Earnings, Price_To_Earnings_Growth, Price_To_Sales, Price_To_Cash_Flow, Price_To_Book_Value, Debt_To_Equity, Return_On_Equity, Return_On_Assets, Profit_Margin, Dividend_Payout, Current_Assets_To_Liabilities, Quick, Interest_Coverage, Asset_Turnover, Inventory_Turnover, Dividend_Yield) VALUES (" + 
			#stock.upper() + ", "
		#cursor.execute(exeSQL) 
		#return {"Symbol": stock.upper(), "Dividend Yield": inputDividendYield}
		return "Stock does not exist in database"

class daily(Resource):
	def get(self, stock):
		dailySQL = "SELECT Symbol, CloseDate, ClosePrice FROM Daily_Stocks;"
		cursor = cnxn.cursor()
		cursor.execute(dailySQL)
		daily = cursor.fetchall()
		dailyList = []
		for i in daily:
			if str(i[0].upper()) == stock.upper():
				dailyList.append({'Close Date': int(i[1]), 'Close Price': i[2]})
		test = str(dailyList)
		test = test.replace("[", "{")
		test = test.replace("]", "}")
		output = {"Symbol": stock.upper(),"Historical": test}
		
		return output
	def put(self, stock):
		inputCloseDate = request.args.get('closedate')
		inputClosePrice = request.args.get('closeprice')
		inputStock = stock.upper()
		inputTransactionID = 1 #Create a Transaction ID somehow

		cursor = cnxn.cursor()
		cursor.execute("INSERT INTO Daily_Stocks (Symbol, CloseDate, ClosePrice) VALUES (?, ?, ?);", inputStock, int(inputCloseDate), float(inputClosePrice))
		cursor.commit()

		return {"Symbol": inputStock, "Close Date": inputCloseDate, "Close Price": inputClosePrice}
	def delete(self, stock):
		inputCloseDate = request.args.get('closedate')
		inputClosePrice = request.args.get('closeprice')
		inputStock = stock.upper()

		cursor = cnxn.cursor()
		cursor.execute("DELETE FROM Daily_Stocks WHERE Symbol = ? AND CloseDate = ? AND ClosePrice = ?;", inputStock, int(inputCloseDate), float(inputClosePrice))
		cursor.commit()

		return {"Symbol": inputStock, "Close Date": inputCloseDate, "Close Price": inputClosePrice}
class chunkDaily(Resource):
	def get(self):
		dailySQL = "SELECT Symbol, CloseDate, ClosePrice FROM Daily_Stocks;"
		cursor = cnxn.cursor()
		cursor.execute(dailySQL)
		daily = cursor.fetchall()
		dailyList = []
		for i in daily:
			dailyList.append([str(i[0].upper()), int(i[1]), i[2]])
		dailyJson = []
		for i in dailyList:
			dailyJson.append({"Symbol": i[0], "Close Date": i[1], "Close Price": i[2]})
		return dailyJson

class prediction(Resource):
	def get(self):
		predictSQL = "SELECT Symbol, Prediction_Short, Prediction_Medium, Prediction_Long FROM Prediction_Cache;"
		cursor = cnxn.cursor()
		cursor.execute(predictSQL)
		predict = cursor.fetchall()
		predictList = []
		for i in predict:
			predictList.append([str(i[0].upper()), i[1], i[2], i[3]])
		predictJson = []
		for i in predictList:
			predictJson.append({"Symbol": i[0], "Prediction Short": i[1], "Prediction Medium": i[2], "Prediction Long": i[3]})
		return predictJson
	def put(self):
		inputSymbol = str(request.args.get('symbol')).upper()
		inputShort = request.args.get('short')
		inputMedium = request.args.get('medium')
		inputLong = request.args.get('long')

		cursor = cnxn.cursor()
		cursor.execute("INSERT INTO Prediction_Cache (Symbol, Prediction_Short, Prediction_Medium, Prediction_Long) VALUES (?, ?, ?, ?);", inputSymbol, inputShort, inputMedium, inputLong)
		cursor.commit()

		return {"Symbol": inputSymbol, "UserId": inputUserId}
	def delete(self):
		inputSymbol = str(request.args.get('symbol')).upper()
		inputShort = request.args.get('short')
		inputMedium = request.args.get('medium')
		inputLong = request.args.get('long')

		cursor = cnxn.cursor()
		cursor.execute("DELETE FROM Prediction_Cache WHERE Symbol = ? AND CloseDate = ? AND ClosePrice = ? AND TransactionID = ?;", inputSymbol, inputShort, inputMedium, inputLong)
		cursor.commit()

class individualPrediction(Resource):
	def get(self, stock):
		predictSQL = "SELECT Symbol, Prediction_Short, Prediction_Medium, Prediction_Long FROM Prediction_Cache;"
		cursor = cnxn.cursor()
		cursor.execute(predictSQL)
		predict = cursor.fetchall()
		predictList = []
		for i in predict:
			predictList.append([str(i[0].upper()), i[1], i[2], i[3]])
		userList = []
		for i in predictList:
			if i[1] == userid:
				userList.append({"Symbol": i[0], "Prediction Short": i[1], "Prediction Medium": i[2], "Prediction Long": i[3]})
		if userList:
			return userList
		return "No stock data exists for the given stock"
	def put(self, stock):
		return "TODO"

class news(Resource):
	#This class will handle implement the code Cory wrote to pull News data
	def get(self):
		return "TODO"

api.add_resource(test, '/', '/test','/test/')

api.add_resource(user, '/user/login', '/user/login/')
api.add_resource(validateUser, '/user/<string:username>', '/user/<string:username>/')

api.add_resource(followedStocks, '/favorite/<string:username>', '/favorite/<string:username>/')

api.add_resource(stocks, '/stock','/stock/')
api.add_resource(stocksIndividual, '/stock/<string:stock>', '/stock/<string:stock>/')
api.add_resource(stockSymbol, '/stock/symbol','/stock/symbol/')
api.add_resource(stockIndividualSymbol, '/stock/symbol/<string:stock>','/stock/symbol/<string:stock>/')
api.add_resource(stockName, '/stock/name','/stock/name/')
api.add_resource(stockIndividualName, '/stock/name/<string:stock>','/stock/name/<string:stock>/')
api.add_resource(stockPriceToEarnings, '/stock/pricetoearnings','/stock/pricetoearnings/')
api.add_resource(stockIndividualPriceToEarnings, '/stock/pricetoearnings/<string:stock>','/stock/pricetoearnings/<string:stock>/')
api.add_resource(stockPriceToEarningsGrowth, '/stock/pricetoearningsgrowth','/stock/pricetoearningsgrowth/')
api.add_resource(stockIndividualPriceToEarningsGrowth, '/stock/pricetoearningsgrowth/<string:stock>','/stock/pricetoearningsgrowth/<string:stock>/')
api.add_resource(stockPriceToSales, '/stock/pricetosales', '/stock/pricetosales/')
api.add_resource(stockIndividualPriceToSales, '/stock/pricetosales/<string:stock>', '/stock/pricetosales/<string:stock>/')
api.add_resource(stockPriceToCashFlow, '/stock/pricetocashflow', '/stock/pricetocashflow/')
api.add_resource(stockIndividualPriceToCashFlow, '/stock/pricetocashflow/<string:stock>', '/stock/pricetocashflow/<string:stock>/')
api.add_resource(stockPriceToBookValue, '/stock/pricetobookvalue', '/stock/pricetobookvalue/')
api.add_resource(stockIndividualPriceToBookValue, '/stock/pricetobookvalue/<string:stock>', '/stock/pricetobookvalue/<string:stock>/')
api.add_resource(stockDebtToEquity, '/stock/debttoequity', '/stock/debttoequity/')
api.add_resource(stockIndividualDebtToEquity, '/stock/debttoequity/<string:stock>', '/stock/debttoequity/<string:stock>/')
api.add_resource(stockReturnOnEquity, '/stock/returnonequity', '/stock/returnonequity/')
api.add_resource(stockIndividualReturnOnEquity, '/stock/returnonequity/<string:stock>', '/stock/returnonequity/<string:stock>/')
api.add_resource(stockReturnOnAssets, '/stock/returnonassets', '/stock/returnonassets/')
api.add_resource(stockIndividualReturnOnAssets, '/stock/returnonassets/<string:stock>', '/stock/returnonassets/<string:stock>/')
api.add_resource(stockProfitMargin, '/stock/profitmargin', '/stock/profitmargin/')
api.add_resource(stockIndividualProfitMargin, '/stock/profitmargin/<string:stock>', '/stock/profitmargin/<string:stock>/')
api.add_resource(stockDividendPayout, '/stock/dividendpayout', '/stock/dividendpayout/')
api.add_resource(stockIndividualDividendPayout, '/stock/dividendpayout/<string:stock>', '/stock/dividendpayout/<string:stock>/')
api.add_resource(stockCurrentAssetsToLiabilities, '/stock/currentassetstoliabilities', '/stock/currentassetstoliabilities/')
api.add_resource(stockIndividualCurrentAssetsToLiabilities, '/stock/currentassetstoliabilities/<string:stock>', '/stock/currentassetstoliabilities/<string:stock>/')
api.add_resource(stockQuick, '/stock/quick', '/stock/quick/')
api.add_resource(stockIndividualQuick, '/stock/quick/<string:stock>', '/stock/quick/<string:stock>/')
api.add_resource(stockInterestCoverage, '/stock/interestcoverage', '/stock/interestcoverage/')
api.add_resource(stockIndividualInterestCoverage, '/stock/interestcoverage/<string:stock>', '/stock/interestcoverage/<string:stock>/')
api.add_resource(stockAssetTurnover, '/stock/assetturnover', '/stock/assetturnover/')
api.add_resource(stockIndividualAssetTurnover, '/stock/assetturnover/<string:stock>', '/stock/assetturnover/<string:stock>/')
api.add_resource(stockInventoryTurnover, '/stock/inventoryturnover', '/stock/inventoryturnover/')
api.add_resource(stockIndividualInventoryTurnover, '/stock/inventoryturnover/<string:stock>', '/stock/inventoryturnover/<string:stock>/')
api.add_resource(stockDividendYield, '/stock/dividendyield', '/stock/dividendyield/')
api.add_resource(stockIndividualDividendYield, '/stock/dividendyield/<string:stock>', '/stock/dividendyield/<string:stock>/')

api.add_resource(daily, '/daily/<string:stock>', '/daily/<string:stock>/')
#api.add_resource(chunkDaily, '/daily', '/daily/')

#api.add_resource(prediction, '/predict', '/predict/', '/prediction', '/prediction/')
#api.add_resource(individualPrediction, '/predict/<string:stock>', '/predict/<string:stock>/', '/prediction/<string:stock>', '/prediction/<string:stock>/')

#api.add_resource(news, '/news', '/news/')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4567, debug=False)

