from racerapi.modules.health.repo import HealthRepo


class HealthService:
    def __init__(self, repo: HealthRepo):
        self.repo = repo

    def check(self) -> dict[str, str]:
        db_ok = self.repo.database_ready()
        return {
            "status": "ok",
            "database": "up" if db_ok else "down",
        }
