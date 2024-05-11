# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pymongo
import json
from bson.objectid import ObjectId
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import psycopg2


class JSONBookstorePipeline:
    def open_spider(self, spider):
        self.file = open('JsonBookData.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    
    def close_spider(self, spider):
        self.file.close()

class CSVBookstorePipeline:
    def process_item(self, item, spider):
        self.file = open('bookdata.csv','a', encoding='')
        line = ''
        line += item["bookName"]
        line += '$' + item["price"] 
        line += '$' + item["stock"] 
        line += '$' + item["descrip"] 
        line += '$' + item["rating"] 
        line += '\n'
        self.file.write(line)
        self.file.close
        return item

class MongoBookstorePipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb+srv://chitin:13082002Tin@cluster0.mxyeorf.mongodb.net/')
        self.db = self.client['bigdata']
    
    def process_item(self, item, spider):
        collection = self.db['book']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")
        pass


class MySQLBookstorePipeline:
    def __init__(self):
        # Thông tin kết nối csdl
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'bookscrapy',
           
        )

        # Tạo con trỏ để thực thi các câu lệnh
        self.cur = self.conn.cursor()

        # Tạo bảng chứa dữ liệu nếu không tồn tại
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bookScrapy (
                id BIGINT NOT NULL AUTO_INCREMENT,
                bookname VARCHAR(255),
                cost VARCHAR(255),
                stock TEXT,
                description TEXT,
                BookUrl VARCHAR(255),
                rating VARCHAR(255),
                PRIMARY KEY (id)            
            )
        """)

    def process_item(self, item, spider):
        # Kiểm tra xem khoá học đã tồn tại chưa
        self.cur.execute("SELECT * FROM bookScrapy WHERE bookname = %s", (str(item['bookName']),))
        result = self.cur.fetchone()

        ## Hiện thông báo nếu đã tồn tại trong csdl
        if result:
            spider.logger.warn("Item đã có trong csdl MySQL: %s" % item['bookName'])


        ## Thêm dữ liệu nếu chưa tồn tại
        else:
            # Định nghĩa cách thức thêm dữ liệu
            self.cur.execute(""" INSERT INTO bookScrapy(bookname, cost, stock, description, BookUrl, rating) 
                                VALUES (%s, %s, %s, %s, %s, %s)""", (
                                str(item['bookName']), 
                                str(item['price']), 
                                str(item["stock"]), 
                                str(item["descrip"]), 
                                str(item['bookURL']), 
                                str(item["rating"]),))

            # Thực hiện insert dữ liệu vào csdl
            self.conn.commit()
        return item

    def close_connect(self, spider):
        # Đóng kết nối csdl
        self.cur.close()
        self.conn.close()

class PostgresBookstorePipeline:
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = '13082002'
        database = 'bookScrapy'

        self.conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.conn.cursor()

        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS bookScrapy (
                            id SERIAL PRIMARY KEY,
                            bookname VARCHAR(255),
                            cost VARCHAR(255),
                            stock TEXT,
                            description TEXT,
                            rating VARCHAR(255),
                            BookUrl VARCHAR(255)
                        );
                        """)

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM bookscrapy WHERE bookname = %s", (str(item['bookName']),))
        result = self.cur.fetchone()

        if result: 
            spider.logger.warn("Khoá học đã tồn tại trên csdl: %s" % item['bookName'])

        else:
            self.cur.execute(""" INSERT INTO bookScrapy(bookname, cost, stock, description, BookUrl, rating) 
                                    VALUES (%s, %s, %s, %s, %s, %s)""", (
                                    str(item['bookName']), 
                                    str(item["price"]), 
                                    str(item["stock"]), 
                                    str(item["descrip"]), 
                                    str(item["bookURL"]), 
                                    str(item['rating']),))
            
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
