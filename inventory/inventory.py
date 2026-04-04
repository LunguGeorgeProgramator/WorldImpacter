import json
from inventory.inventory_item import InventoryItem 

class Inventory:

    def __init__(self):
        self.invetory_json_path = "inventory/inventory_storage.json"
        self.inventory_items = []
        self._load_inventory()

    def _load_inventory(self):
        with open(self.invetory_json_path) as f:
            for json_item in json.load(f):
                self.inventory_items.append(InventoryItem(
                    json_item['id'],
                    json_item['name'],
                    json_item['count'],
                    json_item['description'], 
                ))
    
    def get_item(self, item_id):
        for item in self.inventory_items:
            if item_id == item.id:
                return item

    