from app.repositories.base_repository import BaseRepository
class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_paginated(self, limit:int = 20, offset:int = 0):
        return self.repository.get_paginated(limit=limit, offset=offset)
    
    def get_paginated_with_conditions(self, conditions: dict, limit:int = 20, offset:int = 0):
        return self.repository.get_paginated_with_conditions(conditions=conditions, limit=limit, offset=offset)
