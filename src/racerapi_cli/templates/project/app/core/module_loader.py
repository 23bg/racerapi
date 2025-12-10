
import importlib
import pkgutil
from fastapi import FastAPI


def load_modules(fastapi_app: FastAPI) -> None:
    """
    Recursively auto-discover all feature modules under app.modules
    and register their routers from api/http.py.
    """

    try:
        from app import modules as modules_package
    except ImportError as e:
        print("❌ Could not import app.modules:", e)
        return

    print("✅ Scanning modules in app/modules (recursive)...")

    for module in pkgutil.walk_packages(
        modules_package.__path__,
        modules_package.__name__ + "."
    ):
        module_name = module.name
        print(f"➡️  Found module: {module_name}")

        # ✅ Only register real http router modules
        if not module_name.endswith(".api.http"):
            continue

        try:
            api_module = importlib.import_module(module_name)

            router = getattr(api_module, "router", None)
            if router is None:
                print(f"⚠️  {module_name} has no 'router' exported — skipping")
                continue

            fastapi_app.include_router(router)
            print(f"✅ Registered router from: {module_name}")

        except Exception as e:
            print(f"❌ Failed loading module {module_name}: {e}")
