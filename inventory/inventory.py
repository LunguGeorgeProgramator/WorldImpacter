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
    
    def get_item_by_name(self, item_name):
        for item in self.inventory_items:
            if item_name == item.name:
                return item


    def add_to_inventory(self, item_name, count=0):
        for item in self.inventory_items:
            if item.name == item_name:
                item.incease_item_count(count)
                self._save_inventory()
                return

        new_item = InventoryItem(len(self.inventory_items) + 1, item_name, count, "")
        self.inventory_items.append(new_item)
        self._save_inventory()
    
    def remove_from_inventory(self, item_name, count=0):
        for item in self.inventory_items:
            if item.name == item_name:
                item.decrease_item_count(count)
                self._save_inventory()
                return

        new_item = InventoryItem(len(self.inventory_items) + 1, item_name, count, "")
        self.inventory_items.append(new_item)
        self._save_inventory()

    def _save_inventory(self):
        data = []
        for item in self.inventory_items:
            data.append({
                "id": item.id,
                "name": item.name,
                "count": item.count,
                "description": getattr(item, "description", "")
            })

        with open(self.invetory_json_path, "w") as f:
            json.dump(data, f, indent=4)


        