# Como Importar Juegos no Render

## Problema
Los juegos fueron importados en tu base de datos local, pero el servidor Render tiene una base de datos diferente. Necesitas importar los juegos también en el servidor Render.

## Solución: Usar la URL de Importación (Recomendado para versión gratuita)

### Opción 1: Importar via Web (Sin acceso al Shell)

Si estás usando la versión gratuita del Render y no tienes acceso al Shell, puedes importar los juegos directamente desde el navegador:

1. **Asegúrate de que el código esté desplegado** (haz commit y push si es necesario)
2. **Accede a esta URL en tu navegador:**
   ```
   https://juegos360.onrender.com/importar-juegos/?token=importar123
   ```
3. **Haz clic en el botón "Importar Juegos Ahora"**
4. **Espera unos minutos** mientras se importan los 607 juegos
5. **Verás una página de confirmación** con las estadísticas

Esto importará todos los 607 juegos del índice con precio de 3000 pesos cada uno.

### Opción 2: Importación Automática en el Deploy

El archivo `render.yaml` ya está configurado para importar los juegos automáticamente en cada deploy. Si quieres forzar una nueva importación:

1. Haz un nuevo deploy (push al repositorio o manualmente desde el panel)
2. Los juegos se importarán automáticamente durante el build

### Opción 3: Usar el Shell del Render (Solo si tienes acceso)

Si tienes acceso al Shell del Render:

1. Ve al panel del Render: https://dashboard.render.com
2. Selecciona tu servicio `juegos360`
3. Haz clic en **"Shell"** (en el menú lateral)
4. Ejecuta este comando:
   ```bash
   python manage.py importar_juegos_indice
   ```

### Verificar que Funcionó

1. Accede al admin: https://juegos360.onrender.com/admin/tienda/juego/
2. Deberías ver todos los juegos listados
3. Verifica que todos tengan precio de 3000 pesos

### Si los Juegos No Aparecen

1. **Limpia los filtros**: En el panel derecho del admin, asegúrate de que todos los filtros estén en "Todo"
2. **Limpia la búsqueda**: Deja el campo de búsqueda vacío
3. **Recarga la página**: Presiona `Ctrl+F5` (o `Cmd+Shift+R` en Mac)
4. **Verifica la paginación**: Si hay más de 100 juegos, usa los enlaces de paginación en la parte inferior

### Comando de Verificación

También puedes verificar cuántos juegos hay en la base de datos ejecutando:

```bash
python manage.py verificar_admin
```

Este comando mostrará:
- Total de juegos
- Juegos disponibles
- Juegos con precio 3000
- Primeros 5 juegos como ejemplo

## Notas Importantes

- El comando `importar_juegos_indice` no duplicará juegos que ya existen (usa `get_or_create`)
- Si un juego ya existe, solo actualizará el precio a 3000 si es diferente
- Todos los juegos se crearán con precio de 3000 pesos
- Las imágenes serán URLs placeholder (puedes actualizarlas después desde el admin)

