from flask import Flask, request
from flask_restful import Resource, Api
import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=JON;DATABASE=stocksSimplified;')
#print("Connected to database.")

app = Flask(__name__)
api = Api(app)

#MySQL
#mysql://scott:tiger@localhost/mydatabase
#Post Gres
#postgresql://scott:tiger@localhost/mydatabase

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
		return "test"

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

	def put(self):
		return stock

class stocksIndividual(Resource):
	def get(self, stockSymbol):
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
			if i[0] == stockSymbol.upper():
				return {"Symbol": i[0], "Name": i[1], "Sector": i[2], "Industry": i[3], "Price To Earnings": i[4], "Price To Earnings Growth": i[5], "Price To Sales": i[6], "Price To Cash Flow": i[7], "Price To Book Value": i[8], "Debt To Equity": i[9], "Return On Equity": i[10], "Return On Assets": i[11], "Profit Margin": i[12], "Dividend Payout": i[13], "Current Assets To Liabilities": i[14], "Quick": i[15], "Interest Coverage": i[16], "Asset Turnover": i[17], "Inventory Turnover": i[18], "Dividend Yield": i[19]}

		return "Stock not in database"

	def put(self):
		return stock

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
		nameJson=[]
		for names in nameList:
			nameJson.append({"Name": names})

		return nameJson
class stockIndividualName(Resource):
	def get(self, stock):
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
		for names in nameList:
			if names == stock:
				return {"Name": names}

		return "Stock does not exist in database"


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

api.add_resource(test, '/', '/test','/test/')
#api.add_resource(user, '/user')
#api.add_resource(followedStocks, '/favorite')
api.add_resource(stocks, '/stock','/stock/')
api.add_resource(stocksIndividual, '/stock/<string:stockSymbol>', '/stock/<string:stockSymbol>/')
api.add_resource(stockSymbol, '/stock/symbol','/stock/symbol/')
api.add_resource(stockIndividualSymbol, '/stock/symbol/<string:stock>','/stock/symbol/<string:stock>/')
api.add_resource(stockName, '/stock/name','/stock/name/')
api.add_resource(stockIndividualName, '/stock/name/<string:stock>','/stock/name/<string:stock>/')
#api.add_resource(daily, '/daily')
#api.add_resource(prediction, '/predict')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=False)

