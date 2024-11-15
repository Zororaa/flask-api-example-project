#import uuid
#from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db # importing sql alchemy database
from models import ItemModel # relating to database 

blp = Blueprint("item", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # Get Items 
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id) # checks for data and manages error handling get_or_404
        return item

    # Delete Items
    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id) # checks for data and manages error handling get_or_404
        db.session.delete(item)
        db.session.commit()
        return{"message": "Item deleted."}
        #raise NotImplementedError("Deleting an item is not implmented")

    # Update Items
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
       item = ItemModel.query.get(item_id) # checks for data and manages error handling get_or_404
       #raise NotImplementedError("Updating an item is not implmented")
       if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
       else:
            item = ItemModel(id=item_id, **item_data)

       db.session.add(item)
       db.session.commit()

       return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(refresh=True) # Set refresh Token expiry
    @blp.arguments(ItemSchema) # From Mashmallow by importing schemas
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        # Need to include rollback if there is an error
        try:    
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")

        return item



