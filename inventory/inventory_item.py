
class InventoryItem:

    def __init__(self, id, name, count = 0, description = None):
        self.id = id
        self.name = name 
        self.count = count
        self.description = description

    def incease_item_count(sef, count = 0):
        if count == 0:
            self.count += 1
        else:
            self.count = count
    
    def set_item_description(sef, description):
        self.description = description
        