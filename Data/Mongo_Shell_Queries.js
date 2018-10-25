db.getCollection("Stock_List").find({})
db.Price_History.find({})
db.Stock_List.find({})
db.BalanceSheet.find({})


//Inserting into DB
db.Price_History.insert({'_id': 'HDFC', Date:{'Close':90, 'Vol' :1000} })
db.ETUrls.insert()

//Deleting Data From DB with Object id 
db.Price_History.deleteOne({"_id" : ObjectId("5b48a711634b76fc1bfd8f1a")})

//Deleting All records from the Table
db.Price_History.deleteMany({})


//Update
db.Stock_List.update({"_id":'Stock_List'} , {$set:{'Ranjith':'Data Analyst'}})
db.ETUrls.update({"_id":'Url'} , {$set:{'StockSplit':"https://economictimes.indiatimes.com/infosys-ltd/infocompanysplits/companyid-Code.cms"}})

//Count Total Rows
db.BalanceSheet.count()
db.Stock_List.count()
db.Price_History.count()

//find with Filter 
db.BalanceSheet.find({"_id":"SUPREMEIND"})
db.Price_History.find({"_id":ISODate("2016-03-04T00:00:00.000+0000")}, {"ELAND":1})

//delete a row 
db.Stock_List.remove({"_id":"SYMBOL"})

//Limit Number of Rows Quering 
db.Stock_List.find({}).limit(5)

//Show Particular Value from SubDocument 
db.BalanceSheet.find({},{"Mar_13.Share_Capital":1})

// Using in 
db.BalanceSheet.find({"_id" : {$in: ["HDFC", "SBIN"] }})

//Delete using Defined List 
Errored_Stock_List = ['ITDCEM', 'NESTLEIND', 'TAKE', 'SANOFI', 'SHARONBIO', 'AEGISCHEM', 'ACCELYA',
                      'CRISIL', 'VBL', 'SCHAEFFLER', 'VIDEOIND', 'MERCK', 'PALASHSECU', 'DICIND',
                      'RSYSTEMS', 'ALBERTDAVD', 'AMBUJACEM', 'PAPERPROD', 'MAXVIL', 'GROBTEA', 'TIFIN',
                      'XCHANGING', 'SMSLIFE', 'DCAL', 'GILLETTE', 'LINDEINDIA', 'VARDHACRLC', 'DIGJAMLTD',
                      'RAIN', 'KSBPUMPS', 'HEXAWARE', 'BIGBLOC', 'WSI', 'FOSECOIND', 'ACC', 'SINTEX', 'ABB',
                      'PGHH', 'MAHINDCIE', 'AVADHSUGAR', 'MAGADSUGAR', 'GANGESSECU', 'SIEMENS', 'VESUVIUS',
                      'CASTROLIND']
                      
db.BalanceSheet.find({"_id":{$in:['ITDCEM', 'NESTLEIND', 'TAKE', 'SANOFI', 'SHARONBIO', 'AEGISCHEM', 'ACCELYA',
                      'CRISIL', 'VBL', 'SCHAEFFLER', 'VIDEOIND', 'MERCK', 'PALASHSECU', 'DICIND',
                      'RSYSTEMS', 'ALBERTDAVD', 'AMBUJACEM', 'PAPERPROD', 'MAXVIL', 'GROBTEA', 'TIFIN',
                      'XCHANGING', 'SMSLIFE', 'DCAL', 'GILLETTE', 'LINDEINDIA', 'VARDHACRLC', 'DIGJAMLTD',
                      'RAIN', 'KSBPUMPS', 'HEXAWARE', 'BIGBLOC', 'WSI', 'FOSECOIND', 'ACC', 'SINTEX', 'ABB',
                      'PGHH', 'MAHINDCIE', 'AVADHSUGAR', 'MAGADSUGAR', 'GANGESSECU', 'SIEMENS', 'VESUVIUS',
                      'CASTROLIND']}})   
                                     
db.BalanceSheet.deleteMany({"_id":{$in:['ITDCEM', 'NESTLEIND', 'TAKE', 'SANOFI', 'SHARONBIO', 'AEGISCHEM', 'ACCELYA',
                      'CRISIL', 'VBL', 'SCHAEFFLER', 'VIDEOIND', 'MERCK', 'PALASHSECU', 'DICIND',
                      'RSYSTEMS', 'ALBERTDAVD', 'AMBUJACEM', 'PAPERPROD', 'MAXVIL', 'GROBTEA', 'TIFIN',
                      'XCHANGING', 'SMSLIFE', 'DCAL', 'GILLETTE', 'LINDEINDIA', 'VARDHACRLC', 'DIGJAMLTD',
                      'RAIN', 'KSBPUMPS', 'HEXAWARE', 'BIGBLOC', 'WSI', 'FOSECOIND', 'ACC', 'SINTEX', 'ABB',
                      'PGHH', 'MAHINDCIE', 'AVADHSUGAR', 'MAGADSUGAR', 'GANGESSECU', 'SIEMENS', 'VESUVIUS',
                      'CASTROLIND']}})              

//Date Based Filter 
db.Price_History.find({"_id":ISODate("2013-03-01T00:00:00.000+0000")})


//Sort 
db.Price_History.find({}).sort("_id"-1)

//Exists - is used to filter rows where some column exists 
db.Price_History.find({"ADFFOODS" : {$exists :true}}, {"ADFFOODS" : 1}).count()
db.BalanceSheet.find({"Dec_13":{$exists:true}}).count()


//Like 
db.QlySheet.find({"_id" : "ELAND"})