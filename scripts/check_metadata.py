from racerapi.app import create_app
from racerapi.db.base import Base

app = create_app()
print('tables:', sorted(Base.metadata.tables.keys()))
