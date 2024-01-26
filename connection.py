import os
from pymongo import MongoClient

class ConecctionMongoDB:
    def __init__(self, user, password, cluster, db, collection):
        self.__user = user
        self.__password = password
        self.__cluster = cluster
        self.__database_name = db
        self.__collection_name = collection
        self.__uri_conexion = f'mongodb+srv://{self.__user}:{self.__password}@{self.__cluster}/{self.__database_name}?retryWrites=true&w=majority'
        self.__client = MongoClient(self.__uri_conexion)
        self.__db = self.__client[self.__database_name]
        self.__collection = self.__db[self.__collection_name]
    
    def upload_document(self, document):
        self.__collection.insert_one(document)
    
    def obtain_document(self, key, id):
        return self.__collection.find_one({key: id})
    
    def update_document(self, key, id, documento):
        self.__collection.update_one({key: id}, {'$set': documento})
    
    def delete_document(self, key, id,):
        self.__collection.delete_one({key: id})
    
    def count_documents(self, key, id):
        return self.__collection.count_documents({key: id})
