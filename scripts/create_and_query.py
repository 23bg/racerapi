from racerapi.db.session import get_engine
from racerapi.db.base import Base
from sqlalchemy import text

engine = get_engine()
Base.metadata.create_all(bind=engine)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
    print('tables from DB:')
    for r in rows:
        print(r[0])
print('Engine url:', str(engine.url))
print('Metadata tables:', sorted(Base.metadata.tables.keys()))
