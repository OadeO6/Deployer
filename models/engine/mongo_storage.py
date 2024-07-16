from os import getenv
from pymongo import MongoClient, ASCENDING
from models.user import User
from models.build import Build
from models.project import Project




class MongoStorage:
    """
    mongodb storage model
    """

    def __init__(self):
        """
        init
        """
        DB_NAME = getenv("DB_NAME", "alx")
        DB_PORT = getenv("DB_PORT", "27017")
        try:
            DB_PORT = int(DB_PORT)
        except Exception as e:
            DB_PORT = 27017
        DB_HOST = getenv("DB_HOST", "localhost")
        self.intransaction = False
        try:
            self.client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = self.client[DB_NAME]
            self.db.user.create_index([("id", ASCENDING)], unique=True)
            self.db.user.create_index([("email", ASCENDING)], unique=True)
            self.db.build.create_index([("id", ASCENDING), ("build_num", ASCENDING)], unique=True)
            self.db.project.create_index([("id", ASCENDING)], unique=True)
            self.db.project.create_index([("user_id", ASCENDING), ("name", ASCENDING)], name="uniq_project", unique=True)
            self.db.ports.create_index([("port", ASCENDING)], unique=True)
        except Exception:
            print("No database connection available")
            exit()
        """
        self.project = db.project.create_index([("_id", ASCENDING)], unique=True)
        self.build = db.build.create_index([("_id", ASCENDING)], unique=True)
        """

    def get_session(self):
        """
        get session
        """
        if hasattr(self, "session"):
            if not self.session.has_ended:
                return self.session
        client = self.client
        self.session = client.start_session()
        return self.session

    def find(self, cls, obj={}, resFilter=None):
        """
        get all data that match
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.find(obj, resFilter)
        return result

    def findOne(self, cls, obj={}, resFilter=None):
        """
        get all data that match
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.find_one(obj, resFilter)
        return result

    def new(self, cls, obj):
        """
        insert into the database
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.insert_one(obj)
        return

    def newMany(self, cls, obj):
        """
        insert into the database
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.insert_many(obj)
        return

    def count(self, cls, obj={}):
        """
        count document by filter
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.count_documents(obj)
        return result

    def delete(self, cls, obj):
        """
        delete matching document
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.delete_many(obj)
        return result.deleted_count

    def update(self, cls, obj, newobj):
        """
        update a document
        """
        #session = self.get_session()
        collection = getattr(self.db, cls.name)
        result = collection.update_one(obj, {"$set":newobj})
        return result.matched_count
    """
    def end(self):
        session = self.get_session()
        try:
            session.commit_transaction()
        except Exception as e:
            session.abort_transaction()
        finally:
            session.end_session()
            self.intransaction = False
        return"""
