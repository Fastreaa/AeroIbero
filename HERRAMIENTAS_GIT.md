# Validación de conflictos de merge

Para evitar commits con marcadores de conflicto (`<<<<<<<`, `=======`, `>>>>>>>`):

1. Ejecuta manualmente:

```bash
python3 scripts_check_conflicts.py
```

2. Instala el hook local una sola vez:

```bash
git config core.hooksPath .githooks
```

Con eso, antes de cada commit se ejecutará la validación y bloqueará commits rotos.
