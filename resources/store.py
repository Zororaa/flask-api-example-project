#import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema
from db import db # importing sql alchemy database
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel # relating to database 


blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented.")
            
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")

        return store