class UserService:
    def get_items(self):
        return []

    def create_item(self, data: dict):
        if not data:
            raise ValueError("Invalid data")
        return {"id": 1, **data}
