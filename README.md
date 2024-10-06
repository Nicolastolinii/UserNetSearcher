# USRNETSEARCHER:
UserNetSearcher es una herramienta de búsqueda de nombres de usuario que permite verificar la disponibilidad de un nombre en múltiples redes sociales. Utiliza conexiones asíncronas para hacer consultas simultáneas, lo que mejora la eficiencia en la recolección de datos sobre el usuario especificado.

## Características

- Consulta múltiples redes sociales en una sola ejecución.
- Uso de peticiones asíncronas para optimizar el tiempo de respuesta.
- Manejo de errores para situaciones comunes (usuario no encontrado, errores de conexión, etc.).
- Salida colorida y formateada en la consola para una mejor legibilidad.


### Instalación:
Primero, asegúrate de tener ``Python`` y ``pip`` instalados. Luego, instala las dependencias necesarias:

```bash
python -m pip install -r requirements.txt
```
##### Uso en Windows:
Para evitar problemas con los colores ANSI en la consola de Windows, habilita el soporte de colores usando el siguiente comando:
```bash
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
```
### Ejecucion:
```bash
python usernetsearcher.py
```

### Ejemplos de Salida:
```
┌──────────────────────────────────────────────────────────────────────────────┐
| Scanned Username: "username"                                                 |
|------------------------------------------------------------------------------|
| SITE            | URL                                                        |
|------------------------------------------------------------------------------|
| facebook        | https://facebook.com/"username"                            |
| twitter         | https://twitter.com/"username"                             |
| instagram       | https://instagram.com/"username"                           |
| linkedin        | https://linkedin.com/in/"username"                         |
| github          | https://github.com/"username"                              |
| pinterest       | https://pinterest.com/"username"                           |
| tiktok          | https://tiktok.com/@username                               |
| reddit          | https://reddit.com/user/"username"                         |
| youtube         | https://youtube.com/c/username                             |
| snapchat        | https://snapchat.com/add/username                          |
| tumblr          | https://username.tumblr.com                                |
| discord         | https://discord.com/users/username                         |
└──────────────────────────────────────────────────────────────────────────────┘

```
## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo [LICENSE](LICENSE).


