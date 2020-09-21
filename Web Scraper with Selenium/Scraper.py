#Import the library
from selenium import webdriver
import pandas as pd
import pymongo
import mysql.connector as connection

class Web_Scrapper():
    def __init__(self,driver:webdriver,driver_path:str,url:str):
        self.driver=driver
        self.driver_path=driver_path
        self.url=url

    def open_website(self):
        self.driver.get(self.url)
    def scrap_data(self):
        prduct_boxes=self.driver.find_elements_by_xpath("//div[contains(@class,'s-include-content-margin s-border-bottom s-latency-cf-section')]")    
        prod_details=[]
        try:
            for product in prduct_boxes:
                proddetails=product.text
                prod_details.append(proddetails.split('\n'))
            cols=['iPhoneName','NoOfRating','Price','Emi','Days','Delivery_Date','DeliveryAmazon']
            df_data=pd.DataFrame(prod_details)
            df_data=df_data.iloc[:,:-1]
            df_data.columns=cols
            print(df_data.head(15))
            #save data
            df_data.to_csv("Review.csv")
            return df_data
        
        except Exception as e:
            print("Element could not be found due to Error: ", e)
            self.driver.close
    def feed_data_mongodb(self,df_data):
        try:
            db_conn=pymongo.MongoClient("mongodb://localhost:27017/")
            db=db_conn['ScraperDB']
            
            collection=db['Scraper']

            records={'iPhoneName':df_data.iloc[:,0].tolist(),
            'NoOfRating':df_data.iloc[:,1].tolist(),'Price':df_data.iloc[:,2].tolist(),
            'Emi':df_data.iloc[:,3].tolist(),'Days':df_data.iloc[:,4].tolist(),
            'Delivery_Date':df_data.iloc[:,5].tolist(),'DeliveryAmazon':df_data.iloc[:,6].tolist()}
            x=collection.insert_one(records)

            print(x.inserted_id)
            results=collection.find({})
            for res in results:
                print(res)
        except Exception as e:
            print("Erro found:",e)
            self.driver.close
    def feed_data_mysql(self,df_data):
        try:
            #connect Mysql database
            mydb=connection.connect(host='localhost',database='webscraper',user='root',passwd='Mysql@123',use_pure=True)
            #check connection whether is connected or not
            print(mydb.is_connected())
            #write a query
            query="CREATE TABLE IF NOT EXISTS Review(iPhoneName VARCHAR(100),NoOfRating VARCHAR(100),Price VARCHAR(100),"\
                   "Emi VARCHAR(100),Days VARCHAR(100),Delivery_Date VARCHAR(100),DeliveryAmazon VARCHAR(100));"
            
            curser=mydb.cursor() #create a curser to excute a query
            curser.execute(query)
            print("Created table")

            #loop through insert record in table
            for row in range(df_data.shape[0]):
                list_=f"'{df_data.iloc[row,0]}','{df_data.iloc[row,1]}','{df_data.iloc[row,2]}','{df_data.iloc[row,3]}','{df_data.iloc[row,4]}','{df_data.iloc[row,5]}','{df_data.iloc[row,6]}'"
                print(list_)
                curser.execute("INSERT INTO Review values({values})".format(values=(list_)))
            mydb.commit()

            #Read data from Mysql
            qry="Select * from Review"

            #store in dataframe
            df_result=pd.read_sql(qry,mydb)
            print(df_result)

            #Loop through get the data
            curser.execute(qry)

            for result in curser.fetchall():
                print(result)

            curser.close()
            mydb.close()

        except Exception as e:  
            print("Error found :",e)
            self.driver.close

if __name__ == "__main__":
    driver_path="./chromedriver"
    url="https://www.amazon.in/s?k=iphone&ref=nb_sb_noss_2"
    driver=webdriver.Chrome(executable_path=driver_path)
    ws=Web_Scrapper(driver,driver_path,url)
    ws.open_website()
    df_data= ws.scrap_data()
    ws.feed_data_mongodb(df_data)
    ws.feed_data_mysql(df_data)
    driver.close