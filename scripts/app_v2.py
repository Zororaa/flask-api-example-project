from flask import Flask, request
from flask_smorest import abort
import uuid

from db import items, stores


app = Flask(__name__)

# Create Item
# Post Item
@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here not only we need to validate data exists,
    # But also what type of data. Price should be a float,
    # for example.
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item

# List All Items
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# Item_id
# Get Item

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items["item_id"]
    except KeyError:
        abort(404, message="Item not found.")

# Delete Item with variable string
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]

        # https://blog.teclado.com/python-dictionary-merge-update-operators/
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")


# Get Store ID
@app.get("/store/<string:store_id>/")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")


#Create Store

@app.post("/store")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(
            404, 
            message="Bad request. Ensure 'name' is included in the JSON payload"
        )

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(
                400, 
                message=f"Store already exists"
            )

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

# Delete Store and its Store Id

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")



# List Stores
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


#if __name__ == '__main__':
    #app.run(port=80)
   # app.run(host="0.0.0.0", port=5000)  # Adjust the port if necessary