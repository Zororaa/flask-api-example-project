from marshmallow import Schema, fields

#Validation to schema for items using marshmallow

## Able to add Items without the need of the store details for Nested Values
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Float(required=True)
    store = fields.Nested(PlainItemSchema(), dump_only=True)

class ItemUpdateSchema(Schema):
    id = fields.Str()
    name = fields.Str()
   

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

   