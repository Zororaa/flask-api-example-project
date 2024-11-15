#import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema, TagSchema, TagAndItemSchema

from db import db # importing sql alchemy database
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel, ItemModel, TagModel # relating to database 


blp = Blueprint("Tags", "tags", description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")

        return tag


@blp.route("/store/<string:tag_id>")
class Tags(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag



@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class TagsLinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")
        
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")
        
        return {"message": "Item removed from tag", "item": item, "tag": tag}


    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting data to the database")

        return tag


    @blp.response(

        202, 
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."}
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400, 
        description="Return if the tag is assigned to one or more items. The tag is not deleted."
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
              400, 
              message="Could not delete tag. Make sure tag is not associated with any items, try again."
              )


@blp.route("/tags/<string:tag_id>")
class GetTags(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag