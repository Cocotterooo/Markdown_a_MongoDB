import os
from pymongo import MongoClient

class ConecctionMongoDB:
    def __init__(self, user, password, db, collection, cluster):
        self.__user = user
        self.__password = password
        self.__cluster = cluster
        self.__database_name = db
        self.__collection = collection
        self.__uri_conexion = f'mongodb+srv://{self.__user}:{self.__password}@{self.__cluster}/{self.__database}?retryWrites=true&w=majority'
        self.__client = MongoClient(self.__uri_conexion)
        self.__db = self.__client[self.__database_name]
        self.__collection = self.__db[self.__collection_name]
    
    def upload_document(self, document):
        self.__collection.insert_one(document)
    
    def obtener_documentos(self):
        return self.__collection.find()
    
    def obtener_documento(self, key, id):
        return self.__collection.find_one({key: id})
    
    def actualizar_documento(self, key, id, documento):
        self.__collection.update_one({key: id}, {'$set': documento})
    
    def eliminar_documento(self, key, id,):
        self.__collection.delete_one({key: id})
    
    def eliminar_documentos(self):
        self.__collection.delete_many({})
