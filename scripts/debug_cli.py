import traceback
import inspect

import racerapi.cli as cli

print('Imported cli module')
print('Registered commands:', cli.app.registered_commands)

try:
    print('\nDumping registered command callback signatures...')
    for info in cli.app.registered_commands:
        cb = info.callback
        print('\nCommand:', getattr(info, 'name', repr(info)))
        try:
            sig = inspect.signature(cb)
            for pname, param in sig.parameters.items():
                print(' -', pname, 'annotation=', param.annotation, 'default=', param.default)
        except Exception:
            print('  (could not inspect signature)')

    print('\nAttempting to build full click command (this may raise)')
    try:
        # Typer app exposes method to build a click command via call
        cli.app()
    except Exception:
        traceback.print_exc()
    print('\nDone')
except Exception:
    traceback.print_exc()
print('\nFunction defaults and annotations:')
for name in ('run', 'new', 'db'):
    fn = getattr(cli, name, None)
    if fn is None:
        print('no function', name)
        continue
    print('\nFunction', name)
    print('  defaults=', getattr(fn, '__defaults__', None))
    print('  annotations=', getattr(fn, '__annotations__', None))
