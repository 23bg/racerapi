from app.modules.system.service import SystemService


def test_system_service_health():
    """
    Unit test for SystemService.health().
    Ensures the service returns the expected standard structure.
    """

    service = SystemService()

    result = service.health()

    assert isinstance(result, dict)
    assert result == {"status": "ok"}
    assert result["status"] == "ok"
