# Azure Functions to generate fake retail loyalty data

## Introduction
This is an Azure Python Function to generate fake retail data. The main purpose of this function is to support POC/Workshops.

## TO DO
ADD Oauth token instructions to be added to README

## Usage
1. Deploy to Azure Functions (Python)
2. Get the URI(and function key)
3. Call the API from Azure Data Factory, Postman or etc
   1. Function supports POST method only
   2. HTTP Request body:

<b> Trans_date </b>: Minimum trans_date as it is in the code is 01-Jan-2020 any earlier dates will result in HTTP error.

For full customer data on a particular date:
```
{ 
	"trans_date": "2020-09-01",
	"dataDomain" : "customers"	
}
```

For transactions data on a particular date:

```
{ 
	"trans_date": "2020-09-01",
	"dataDomain" : "transactions"	
}
```

<b>Note:</b> Customer data needs to be pre-generated on development environment.
        Customer data is generated for date range 01-Jan-2020 to 01-Sep-2020 but more dates can be generated in development environment. 

        1. Run the function locally
        2. call the API (Locally) for any date in future and the function 
        will generate the data for date plus all days before it.
    
## Data (HTTP Response):

### Customer (JSON):

Customer data is in JSON format and is a full set of all customers in the system for that date which on top of the data from previous day file also includes:
1. Changes to existing customer (for example change email or physical address) to perform CDC (change data capture) operation on it.
2. New customers that do not exists in previous file.

```
    {
        "loyalty_num": "FHMC9479966548886",
        "name": "Dwayne Allen",
        "email": "riddleamanda@hotmail.com.au",
        "dob": "1907-09-29",
        "address": "265 Leon Ramp Callahanview, ACT, 2910",
        "city": "Lake Cheyenneport",
        "state": "South Australia",
        "postCode": "2223",
        "membersince": "2019-01-23"
    },
    {
        "loyalty_num": "CUDP9033540863227",
        "name": "Kevin Ellis",
        "email": "johnsonrichard@yahoo.com",
        "dob": "1998-01-25",
        "address": "65 Jackson Interchange Vincentmouth, ACT, 2355",
        "city": "North Nicholasmouth",
        "state": "Queensland",
        "postCode": "2900",
        "membersince": "2018-12-08"
    },...}
```
### Transactions (CSV):  
Transactions are generated as line items (same invoice number on multiple lines with different SKU).

```
invoiceNumber,timestamp,loyaltyNum,store,sku,uPrice,qty
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,32010,23.0,16
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,04530,16.0,1
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,28063,14.11,25
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,21279,9.65,25
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,20622,28.0,11
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,13878,24.0,24
04ecdef53e2334f82409150b09bca11a,"2020-09-01 21:32:00",PMVK1743599244678,Port Thomas,04661,12.59,3
59c08783825d7b59418ab1c258a68ecf,"2020-09-01 15:34:00",ZNNZ5095231637916,Williamsmouth,17148,31.0,4
59c08783825d7b59418ab1c258a68ecf,"2020-09-01 15:34:00",ZNNZ5095231637916,Williamsmouth,06482,26.2,5
59c08783825d7b59418ab1c258a68ecf,"2020-09-01 15:34:00",ZNNZ5095231637916,Williamsmouth,10937,8.8,24

```


<b>Note:</b> Unlike customer data which are fixed and pre-generated, Transactions data is generated on the fly randomlly. So calling the transactions API for the same date twice could (most likely will) give you different data sets.


## Future improvements:
1. Store and retreive customer data from Azure Blob Storage.
2. Generate customer data not available on storage on API call.