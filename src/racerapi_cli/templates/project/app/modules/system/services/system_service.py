from app.modules.system.domain.app_info import AppInfo

class SystemService:
    def health(self):
        return {"status": "ok"}

    def version(self):
        info = AppInfo()
        return {"name": info.name, "version": info.version}
