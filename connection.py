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
    
    def upload_document(self, document:dict):
        self.__collection.insert_one(document)
    
    def obtain_document(self, key:str, id:str):
        return self.__collection.find_one({key: id})
    
    def update_document(self, key:str, id:str, key_for_replaze:str, new_content:str):
        self.__collection.update_one({key: id}, {'$set': {key_for_replaze: new_content}})
    
    def delete_document(self, key:str, id:str):
        self.__collection.delete_one({key: id})
    
    def count_documents(self, key:str, id:str):
        return self.__collection.count_documents({key: id})
    
    def show_all_for_key(self, key:str):
        return self.__collection.find({}, {'_id': 0, key:1})
