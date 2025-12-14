from app.domain.system import System


def test_system_creation():
    system = System(
        name="MyApp",
        version="0.0.3",
    )

    assert system.name == "MyApp"
    assert system.version == "0.0.3"


def test_system_is_compatible_true():
    system = System(
        name="MyApp",
        version="0.0.3",
    )

    assert system.is_compatible("0.0.1") is True


def test_system_is_compatible_false():
    system = System(
        name="MyApp",
        version="0.0.3",
    )

    assert system.is_compatible("1.0.0") is False
