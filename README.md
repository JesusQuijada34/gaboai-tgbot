# Gabo AI - Telegram Bot para Gestión de Repositorios

## Descripción General

Bot de Telegram automatizado que sincroniza y publica novedades de repositorios desde el catálogo de Jesús Quijada (GitHub: JesusQuijada34/catalog). El bot lee metadatos de repositorios, genera mensajes enriquecidos y los publica automáticamente en canales y grupos configurados.

## Arquitectura del Sistema

### Componentes Principales

1. **Configuración y Persistencia**
   - `config/published.json`: Lista de repositorios ya publicados (evita duplicados)
   - `config/bot.json`: Configuración del bot (token, chat IDs)
   - `config/repo.list`: Archivo local de referencia (la lectura real es remota)

2. **Sincronización Remota**
   - Lee `repo.list` desde `https://raw.githubusercontent.com/JesusQuijada34/catalog/main/repo.list`
   - Parsea repositorios separados por comas
   - Sincronización automática cada 3 minutos

3. **Procesamiento de Metadatos**
   - Extrae información de `details.xml` (nombre, versión, publisher, clasificación por edad)
   - Lee `README.md` para descripciones
   - Detecta páginas web activas en `c/<repo>`

4. **Sistema de Moderación**
   - Filtros de contenido inapropiado
   - Detección de spam y caracteres prohibidos
   - Eliminación automática de mensajes problemáticos

## Funcionamiento Técnico

### Flujo de Sincronización

```python
# 1. Lectura remota de repo.list
repos = read_repo_list_remote()  # GitHub raw API

# 2. Verificación de repos ya publicados
published = load_published()  # config/published.json
new_repos = [repo for repo in repos if repo not in published]

# 3. Procesamiento de cada repo nuevo
for repo in new_repos:
    metadata = get_repo_metadata(repo)  # details.xml + README.md
    message = build_markdown_message(metadata)  # Formato Markdown
    await publish_to_targets(context, message)  # Telegram

# 4. Actualización de estado
save_published(updated_published_list)
```

### Estructura de Datos

#### RepoMetadata (dataclass)
```python
@dataclass
class RepoMetadata:
    name: str                    # Nombre del repositorio
    version: Optional[str]       # Versión actual
    publisher: Optional[str]     # Publisher/empresa
    age_rating: Optional[str]    # Clasificación por edad
    repo: str                    # Nombre del repo en GitHub
    description: Optional[str]   # Descripción del README
    repo_url: str               # URL completa del repo
    web_url: Optional[str]      # URL de la web si existe
```

### Sistema de Scheduler

#### Fallback de JobQueue
```python
# Prioridad 1: JobQueue oficial de python-telegram-bot
if getattr(app, "job_queue", None):
    app.job_queue.run_repeating(sync_job, interval=180, first=10)

# Prioridad 2: Scheduler asyncio personalizado
else:
    loop.create_task(_periodic_sync_with_asyncio(app, interval_seconds=180))
```

### Filtros de Moderación

#### Patrones de Detección
```python
PROFANITY_WORDS = {
    "puta", "puto", "mierda", "carajo", "coño", "pinga",
    "fuck", "shit", "bitch", "asshole", "bastard", "dick"
}

SPAM_PATTERNS = [
    r"(?i)free\s+crypto",           # Crypto gratis
    r"(?i)\bwin\b.{0,20}\bprize\b", # Premios/ganancias
    r"(?i)http[s]?://[^\s]+(?:\.ru|\.cn|bit\.ly)", # URLs sospechosas
    r"(?i)\b\$\b.{0,3}\d{2,}"       # Cantidades de dinero
]

BLOCKED_CHARS = {
    "\u200b", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069"  # Zero-width, RTL
}
```

## Configuración

### Variables de Entorno (.env)
```bash
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHANNEL_ID=@tu_canal_o_id_num
TELEGRAM_GROUP_ID=-1001234567890
```

### Configuración del Bot (config/bot.json)
```json
{
  "token": "123456:ABC...",
  "channel_id": "@tu_canal",
  "group_id": "-1001234567890"
}
```

### Lista de Repositorios
El bot lee automáticamente desde:
```
https://raw.githubusercontent.com/JesusQuijada34/catalog/main/repo.list
```

Formato esperado:
```
repo1,repo2,repo3
# Comentarios permitidos
repo4,repo5
```

## Comandos del Bot

### Comandos Públicos
- `/sync` - Sincronización manual del catálogo
- `/reset` - Limpia la lista de repos publicados
- `/help` - Muestra ayuda

### Comandos de Moderación (Automáticos)
- **Filtro de Contenido**: Elimina mensajes con groserías
- **Anti-Spam**: Detecta y elimina spam automáticamente
- **Anti-Flood**: Controla el flujo de mensajes
- **Filtro de Caracteres**: Bloquea caracteres peligrosos

## Implementación Técnica

### Manejo de Errores
```python
try:
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        return response.text
    return None
except requests.RequestException as exc:
    logger.warning("Network error fetching %s: %s", url, exc)
    return None
```

### Logging Estructurado
```python
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("gaboai-tgbot")
```

### Validación de Sintaxis (Lint Check)
```python
def run_lint_check() -> bool:
    # Prioridad 1: ruff
    # Prioridad 2: pyflakes  
    # Fallback: compilación de sintaxis
    compile(source_code, filename, "exec")
```

### Parsing XML Robusto
```python
def parse_details_xml(xml_text: str) -> Tuple[...]:
    try:
        root = etree.fromstring(xml_text.encode("utf-8"))
        name = root.findtext("name")
        version = root.findtext("version")
        publisher = root.findtext("publisher") or root.findtext("author")
        age_rating = root.findtext("age") or root.findtext("age_rating")
        return name, version, publisher, age_rating
    except Exception as exc:
        logger.warning("Failed parsing details.xml: %s", exc)
        return None, None, None, None
```

## Dependencias

### Librerías Principales
- `python-telegram-bot==21.4` - API de Telegram
- `requests==2.32.3` - Cliente HTTP
- `python-dotenv==1.0.1` - Variables de entorno
- `lxml==5.2.2` - Parser XML

### Módulos Estándar
- `asyncio` - Programación asíncrona
- `json` - Serialización de datos
- `logging` - Sistema de logs
- `pathlib` - Manejo de rutas
- `re` - Expresiones regulares
- `subprocess` - Ejecución de comandos
- `sys` - Funcionalidades del sistema
- `xml.etree.ElementTree` - Parser XML estándar

## Instalación y Uso

### 1. Instalar Dependencias
```bash
pip install -r lib/requirements.txt
```

### 2. Configurar Bot
```bash
# Crear .env o config/bot.json
python3 ./gaboai-tgbot.py
# El bot pedirá el token si no está configurado
```

### 3. Ejecutar
```bash
# Linux/macOS
./autorun

# Windows
autorun.bat

# Directo
python3 ./gaboai-tgbot.py
```

## Características de Seguridad

### Validación de Entrada
- Sanitización de URLs
- Validación de metadatos XML
- Control de caracteres peligrosos

### Control de Acceso
- Solo comandos básicos en grupos
- Configuración solo en chat privado
- Logs de todas las acciones

### Protección Anti-Spam
- Detección de patrones maliciosos
- Filtros de contenido automáticos
- Sistema de advertencias

## Monitoreo y Logs

### Niveles de Log
- **INFO**: Operaciones normales, sincronización
- **WARNING**: Errores no críticos, fallos de red
- **ERROR**: Errores críticos, fallos de publicación
- **DEBUG**: Información detallada (configurable)

### Métricas de Rendimiento
- Tiempo de sincronización
- Repositorios procesados
- Mensajes publicados
- Errores y reintentos

## Escalabilidad

### Optimizaciones Implementadas
- Cache de repositorios publicados
- Delays entre publicaciones (0.5s)
- Timeouts de red configurables
- Fallbacks para servicios externos

### Límites y Restricciones
- Máximo 100 repos por sincronización
- Timeout de 15s por petición HTTP
- Intervalo mínimo de 3 minutos entre syncs
- Límite de 600 caracteres por descripción

## Troubleshooting

### Problemas Comunes
1. **Token inválido**: Verificar en @BotFather
2. **Sin permisos**: El bot debe ser admin en el grupo/canal
3. **Errores de red**: Verificar conectividad a GitHub
4. **Lint falla**: Verificar sintaxis del script

### Debug
```bash
# Habilitar logs detallados
export PYTHONPATH=.
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
import gaboai-tgbot
"
```

## Licencia

GPL-2.0-or-later © 2025 Jesús Quijada

## Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama feature
3. Commit de cambios
4. Pull Request

## Contacto

- **Desarrollador**: Jesús Quijada (@JesusQuijada34)
- **GitHub**: https://github.com/JesusQuijada34
- **Proyecto**: Influent Package Manager (IPM)