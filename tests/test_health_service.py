from racerapi.modules.health.service import HealthService


class FakeHealthRepo:
    def __init__(self, ready: bool):
        self.ready = ready

    def database_ready(self) -> bool:
        return self.ready


def test_health_service_reports_up_when_repo_ready():
    service = HealthService(FakeHealthRepo(True))

    result = service.check()

    assert result == {"status": "ok", "database": "up"}


def test_health_service_reports_down_when_repo_not_ready():
    service = HealthService(FakeHealthRepo(False))

    result = service.check()

    assert result == {"status": "ok", "database": "down"}
