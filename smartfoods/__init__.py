import logging
import json
import csv
import random
import pathlib
from datetime import datetime, timedelta
import argparse
import logging
import sys
import time
from faker import Faker
from faker.providers import *
import hashlib
import azure.functions as func



def read_csv(filename):
    items = []
    with open(filename, newline='') as csvfile:
        items_csv = csv.reader(csvfile, delimiter=',')
        next(items_csv)
        for row in items_csv:
            items.append(row)
        logging.info(filename + " imported succssfully")
        return items

def gen_customers(cust_count=2):
    fake = Faker('en_AU')
    fake.seed_instance(4321)
    with open(str(pathlib.Path(__file__).parent)+'customer11.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(cust_count):
            person = fake.simple_profile(sex=None)
            csvwriter.writerow([fake.bban(),person['name'],person['mail'],person['birthdate'],fake.address().replace("\n"," "),fake.city(),fake.state(),fake.postcode(),fake.date_between(start_date="-6y", end_date="today")])

def date_range_gen(EndDate):
    startDate = EndDate
    start = datetime.strptime(startDate, "%Y%m%d")
    notFound = True
    while notFound:
        if not (pathlib.Path(str(pathlib.Path(__file__).parent)+ '/Data/customer/customer_'+start.strftime("%Y%m%d")+'.csv').is_file()):
            start = start - timedelta(days=1)
            if start <= datetime.strptime('20200101', "%Y%m%d"):
                notFound = False
        else:
            notFound = False
    end = datetime.strptime(EndDate, "%Y%m%d")
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days+1)]
    #print(date_generated)
    return date_generated
    
def update_customer_date_range(endDate):
    date_range = date_range_gen(endDate)
    
    
    c = 0
    while (c < len(date_range)-1):
        prevFile = date_range[c].strftime("%Y%m%d")
        currFile = date_range[c+1].strftime("%Y%m%d")
                  
        update_customers(prevFile,currFile)
        c = c + 1
        

def update_customers(customerFile,fileDate,Delta=False):
    fake2 = Faker('en_AU')
    fake2.seed_instance(43212)
    
    
    fake = Faker('en_AU')
    fake.seed_instance(4321)
    with open(str(pathlib.Path(__file__).parent)+'/Data/customer/customer_'+fileDate+'.csv', 'w', newline='') as csvfile:
        try:
            custs = read_csv(str(pathlib.Path(__file__).parent)+'./Data/customer/customer_'+customerFile+'.csv')
        except:
            custs = read_csv('./Data/customer/customer_20200101.csv')
        update_count = int(len(custs)*random.randint(1,20)*0.001)
        insert_count = int(len(custs)*random.randint(0,15)*0.001)
        logging.info("Generating update customer_"+fileDate +".csv file with "+str(update_count)+" updated customers and "+str(insert_count)+" new customers")
        csvwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(update_count):
            whatToChange = random.randint(1,3)
            
            random_cust = random.randint(1,len(custs)-1)
            #print(str(random_cust)+' '+str(whatToChange))
            if (whatToChange == 1):
                #print("hi")
                
                custs[random_cust][4] = fake2.address().replace("\n"," ")
                
            if (whatToChange == 2):
                
                custs[random_cust][2] = fake2.ascii_email()
                
            if (whatToChange == 3):
                custs[random_cust][5] = fake2.city()
                custs[random_cust][6] = fake2.state()
            if(Delta == True):
                csvwriter.writerow(custs[random_cust])
        #print(custs)
        if(Delta == False):
            for customer in custs:
                csvwriter.writerow(customer)
        
            
        for i in range(insert_count):
            person = fake.simple_profile(sex=None)
            csvwriter.writerow([fake.bban(),person['name'],person['mail'],person['birthdate'],fake.address().replace("\n"," "),fake.city(),fake.state(),fake.postcode(),fake.date_between(start_date="-6y", end_date="today")])
def new_lineItem(items):
    rand = random.randint(1,len(items)-1)
    lineItem = {}
    
    lineItem['sku'] = items[rand][0]
    lineItem['desc'] = items[rand][1]
    lineItem['uPrice'] = float(round(random.uniform(1,40),random.randint(0,2)))
    lineItem['foodGroup'] = items[rand][2]
    lineItem['qty'] = random.randint(1,25)
        
    
    return lineItem

def new_transaction(transdate,item_count,items,custs):
    trans = {}
    random_cust = random.randint(1,len(custs)-1)
    if (random.randint(1,100) in [1,20,100]):
        trans['loyaltyNum'] = ''
    else:
        trans['loyaltyNum'] = custs[random_cust][0]
    trans['store'] = custs[random_cust][5]
    trans['timestamp'] = str(datetime.strptime(transdate, '%Y-%m-%d')+timedelta(minutes=random.randint(1,1440)))
    trans['invoiceNumber'] = hashlib.md5((str(datetime.now())+str(random.randint(1,134322442))+str(random.randint(1,134322442))+str(custs[random_cust][0])).encode()).hexdigest()
    trans['items'] = []
    for i in range(item_count):
        trans['items'].append(new_lineItem(items))
    
    return trans





def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        trans_date = req_body.get('trans_date')
    except ValueError:
        return func.HttpResponse(
             "Please pass a transaction date (trans_date) in the request body",
             status_code=400
        )
    
    try:
        dataDomain = req_body.get('dataDomain')
    except:
        return func.HttpResponse(
             "Please pass data domain(dataDomain) in the request body",
             status_code=400
        )    
    
    ### RETURN CUSTOMERS IN JSON FORMAT
    if (dataDomain == 'customers'):
        try:
            filename = str(pathlib.Path(__file__).parent)+ '/Data/customer/customer_'+trans_date.replace('-','')+'.csv'
            with open(filename, newline='') as csvfile:
                items_csv = csv.DictReader(csvfile,fieldnames = ( "loyalty_num","name","email","dob","address","city","state","postCode","membersince" ), delimiter=',')
                #next(items_csv)
                response = json.dumps( [ row for row in items_csv ] )
        except:
            update_customer_date_range(trans_date.replace('-',''))
            filename = str(pathlib.Path(__file__).parent)+ '/Data/customer/customer_'+trans_date.replace('-','')+'.csv'
            with open(filename, newline='') as csvfile:
                items_csv = csv.DictReader(csvfile,fieldnames = ( "loyalty_num","name","email","dob","address","city","state","postCode","membersince" ), delimiter=',')
                #next(items_csv)
                response = json.dumps( [ row for row in items_csv ] )
        return func.HttpResponse(
        #json.dumps(response),
        response,
        mimetype="application/json",
    )
        
    ### RETURN TRANSACTIONS IN CSV FORMAT
    try:
        items = read_csv(str(pathlib.Path(__file__).parent)+ '/Data/food/food.csv')
    except:
        logging.info("Items list file not found")
        return func.HttpResponse(
        "Items file not found",
         status_code=400
        )
    try:
        custs = read_csv(str(pathlib.Path(__file__).parent)+ '/Data/customer/customer_'+trans_date.replace('-','')+'.csv')
    except:
        update_customer_date_range(trans_date.replace('-',''))
        custs = read_csv(str(pathlib.Path(__file__).parent)+ '/Data/customer/customer_'+trans_date.replace('-','')+'.csv')
    


    trans_to_generate = random.randint(1000,2000)
    trans_counter = 0
    total_trans_counter = 1
    transactions = []
    response = ''
    response = response + 'invoiceNumber'+","+'timestamp'+","+'loyaltyNum'+","+'store'+","+'sku'+","+'uPrice'+","+'qty'+"\n"
    

    while (trans_counter <= trans_to_generate):
                trans_counter = trans_counter  + 1
                total_trans_counter = total_trans_counter  + 1
                trans = new_transaction(trans_date,random.randint(1,34),items,custs)
                #transactions.append(trans)
                for item in trans['items']:
                    response = response + trans['invoiceNumber']+",\""+trans['timestamp']+"\","+trans['loyaltyNum']+","+trans['store']+","+item['sku']+","+str(item['uPrice'])+","+str(item['qty'])+"\n"

    #response = {"transactions":transactions}
    return func.HttpResponse(
        #json.dumps(response),
        response,
        mimetype="application/json",
    )
    
    
