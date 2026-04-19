from .controller import router


class UserModule:
	def register(self, app):
		app.include_router(router, prefix="/users")
