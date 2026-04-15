import traceback
import racerapi.cli as c
from typer.main import get_command

print('Loaded racerapi.cli')
try:
    get_command(c.app.info)
    print('get_command succeeded')
except Exception:
    traceback.print_exc()
