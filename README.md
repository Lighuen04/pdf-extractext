# PDF Extractext - Aplicación FastAPI de Grado de Producción

Una aplicación FastAPI orientada a producción para extracción de texto de PDF y resumen con IA usando una **arquitectura empresarial de 3 capas** (API, Aplicación, Infraestructura).

## 🏗️ Descripción General de la Arquitectura

Este proyecto sigue una **arquitectura limpia** con clara separación de responsabilidades:

### Capa 1: **Capa API / Presentación** (`src/api/`)
- **Routes**: Manejadores de puntos finales HTTP (routers de FastAPI)
- **Schemas**: Modelos de solicitud/respuesta de Pydantic para validación
- **Dependencies**: Contenedor de inyección de dependencias para gestión de servicios

### Capa 2: **Capa Aplicación / Servicios** (`src/application/`)
- **Services**: Orquestación de lógica de negocio
- **Use Cases**: Implementación de procesos de negocio específicos
- **DTOs**: Objetos de transferencia de datos para comunicación entre capas

### Capa 3: **Capa Infraestructura / Datos** (`src/infrastructure/`)
- **Database**: Gestión de conexión a MongoDB y ciclo de vida
- **Repositories**: Capa de persistencia de datos con operaciones CRUD
- **Adapters**: Integración con servicios externos (extracción de PDF, resumen con IA)
- **Models**: Esquemas de documentos MongoDB

### Entre Capas: **Configuración** (`src/config/`)
- **Settings**: Gestión de configuración basada en variables de entorno
- **Constants**: Constantes de aplicación global

## 🚀 Inicio Rápido

### Requisitos Previos

- **Python 3.9+**
- **MongoDB 7.0+** (local o Docker)
- **pip** o **poetry** para gestión de dependencias

### Opción 1: Configuración de Desarrollo Local

#### 1. Clonar y Configurar Entorno

```bash
# Navegar al directorio del proyecto
cd pdf-extractext

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Copiar archivo de configuración
cp .env.example .env

# Editar .env para tu configuración local (opcional)
# Los valores por defecto ya están configurados
```

#### 2. Instalar Dependencias

```bash
# Instalar dependencias principales
pip install -e .

# Instalar dependencias de desarrollo (opcional)
pip install -e ".[dev]"
```

#### 3. Iniciar MongoDB

Asegúrate de que MongoDB esté ejecutándose en tu sistema:

```bash
# En Windows (si está instalado como servicio)
net start MongoDB

# En macOS con Homebrew
brew services start mongodb-community

# O ejecutar vía Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ADMIN_USERNAME=admin \
  -e MONGO_INITDB_ADMIN_PASSWORD=password \
  mongo:7.0
```

#### 4. Ejecutar la Aplicación

```bash
# Iniciar el servidor de desarrollo
python main.py

# El servidor se iniciará en http://localhost:8000
```

#### 5. Acceder a la Aplicación

- **Documentación de API (Swagger)**: http://localhost:8000/docs
- **Documentos de API Alternativos (ReDoc)**: http://localhost:8000/redoc
- **Verificación de Estado**: http://localhost:8000/health
- **Punto Final Raíz**: http://localhost:8000/

### Opción 2: Configuración con Docker (Recomendado para Producción)

#### 1. Usando Docker Compose

```bash
# Iniciar todos los servicios (API + MongoDB)
docker-compose up -d

# Ver registros
docker-compose logs -f api

# Detener servicios
docker-compose down

# Eliminar volúmenes (limpiar base de datos)
docker-compose down -v
```

#### 2. Usando Docker de Forma Independiente

```bash
# Construir la imagen
docker build -t pdf-extractext:latest .

# Ejecutar el contenedor
docker run -d \
  --name pdf_extractext_api \
  -p 8000:8000 \
  -e MONGODB_URL="mongodb://mongodb:27017" \
  -e MONGODB_DATABASE="pdf_extractext" \
  --link mongodb:mongodb \
  pdf-extractext:latest
```

## 📁 Estructura del Proyecto

```
pdf-extractext/
├── src/                           # Código fuente
│   ├── api/                       # Capa 1: Presentación
│   │   ├── routes/               # Manejadores de rutas HTTP
│   │   │   ├── health.py         # Punto final de verificación de estado
│   │   │   └── documents.py      # Puntos finales de gestión de documentos
│   │   ├── schemas.py            # Modelos de solicitud/respuesta de Pydantic
│   │   └── dependencies.py       # Contenedor de inyección de dependencias
│   │
│   ├── application/              # Capa 2: Lógica de Aplicación
│   │   ├── services/             # Servicios de negocio
│   │   │   ├── document_service.py
│   │   │   ├── extraction_service.py
│   │   │   └── summarization_service.py
│   │   ├── use_cases/            # Implementaciones de casos de uso
│   │   │   ├── upload_document.py
│   │   │   ├── extract_text.py
│   │   │   └── summarize_text.py
│   │   └── dto/                  # Objetos de transferencia de datos
│   │       └── document_dto.py
│   │
│   ├── infrastructure/           # Capa 3: Infraestructura
│   │   ├── database/             # Gestión de conexión a base de datos
│   │   │   └── connection.py
│   │   ├── repositories/         # Persistencia de datos
│   │   │   ├── base_repository.py
│   │   │   └── document_repository.py
│   │   ├── adapters/             # Integraciones de servicios externos
│   │   │   ├── mongodb_adapter.py
│   │   │   ├── pdf_extractor_adapter.py
│   │   │   └── ai_summarizer_adapter.py
│   │   └── models/               # Esquemas de documentos MongoDB
│   │       └── document_model.py
│   │
│   └── config/                   # Configuración entre capas
│       ├── settings.py           # Configuración basada en variables de entorno
│       └── constants.py          # Constantes de aplicación
│
├── tests/                        # Suite de pruebas
│   ├── unit/                     # Pruebas unitarias
│   │   ├── test_services.py
│   │   └── test_repositories.py
│   ├── integration/              # Pruebas de integración
│   │   └── test_api.py
│   └── conftest.py              # Configuración de Pytest y fixtures
│
├── main.py                       # Punto de entrada de la aplicación
├── pyproject.toml               # Metadatos y dependencias del proyecto
├── Dockerfile                   # Imagen Docker de producción
├── docker-compose.yml           # Configuración de Docker Compose
├── .env.example                 # Plantilla de configuración de entorno
├── .gitignore                   # Reglas de ignorancia de Git
└── README.md                    # Este archivo
```

## 🔌 Puntos Finales de API

### Verificación de Estado
```
GET /health
```
Devuelve el estado de salud de la aplicación y la base de datos.

**Respuesta:**
```json
{
  "status": "healthy",
  "message": "Application is running",
  "version": "0.1.0",
  "database_connected": true
}
```

### Gestión de Documentos
```
POST   /api/v1/documents              # Cargar/crear documento
GET    /api/v1/documents              # Listar documentos
GET    /api/v1/documents/{document_id}  # Obtener detalles del documento
DELETE /api/v1/documents/{document_id}  # Eliminar documento
```

**Ejemplo: Crear Documento**
```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "document.pdf",
    "original_filename": "my_document.pdf",
    "file_size": 2048,
    "file_path": "/uploads/document.pdf"
  }'
```

## 🧪 Pruebas

### Ejecutar Todas las Pruebas

```bash
# Ejecutar todas las pruebas con cobertura
pytest --cov=src --cov-report=html

# Abrir informe de cobertura
open htmlcov/index.html  # macOS
# o fire.exe htmlcov/index.html  # Windows
```

### Ejecutar Categorías de Pruebas Específicas

```bash
# Solo pruebas unitarias
pytest tests/unit/

# Solo pruebas de integración
pytest tests/integration/

# Salida detallada
pytest -v

# Ejecutar una prueba específica
pytest tests/unit/test_services.py::TestDocumentService::test_create_document -v
```

## 🛠️ Flujo de Trabajo de Desarrollo

### Herramientas de Calidad de Código

```bash
# Formatear código con Black
black src/ tests/

# Ordenar importaciones con isort
isort src/ tests/

# Linting
flake8 src/ tests/

# Verificación de tipos con mypy
mypy src/

# Todas las verificaciones a la vez
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Tareas Comunes de Desarrollo

#### Agregar un Nuevo Punto Final

1. **Crea un nuevo router** en `src/api/routes/new_feature.py`
2. **Agrega schemas** en `src/api/schemas.py`
3. **Implementa el servicio** en `src/application/services/`
4. **Implementa el repositorio** en `src/infrastructure/repositories/`
5. **Registra el router** en `main.py`

#### Agregar un Nuevo Servicio

1. Crea la clase de servicio en `src/application/services/`
2. Crea DTOs correspondientes en `src/application/dto/`
3. Implementa el repositorio en `src/infrastructure/repositories/`
4. Agrega al contenedor de inyección de dependencias en `src/api/dependencies.py`

#### Agregar una Nueva Dependencia

1. Actualiza `pyproject.toml` con el nuevo paquete
2. Reinstala: `pip install -e .`
3. Agrega configuración a `src/config/settings.py` si es necesario
4. Crea un adaptador en `src/infrastructure/adapters/` si es un servicio externo

## 📝 Configuración de Entorno

Crea un archivo `.env` desde la plantilla:

```bash
cp .env.example .env
```

Variables de configuración clave:

| Variable | Valor Por Defecto | Descripción |
|----------|---------|-------------|
| `APP_NAME` | "PDF Extractext" | Nombre de la aplicación |
| `DEBUG` | false | Habilitar modo depuración |
| `PORT` | 8000 | Puerto de la aplicación |
| `MONGODB_URL` | mongodb://localhost:27017 | Cadena de conexión a MongoDB |
| `MONGODB_DATABASE` | pdf_extractext | Nombre de la base de datos |
| `API_PREFIX` | /api/v1 | Ruta base de API |
| `MAX_FILE_SIZE_MB` | 100 | Tamaño máximo de archivo de carga |

## 🔐 Consideraciones de Seguridad

- [ ] Habilitar autenticación (no implementado en MVP)
- [ ] Habilitar limitación de velocidad para producción
- [ ] Usar HTTPS en producción
- [ ] Validar y purificar toda la entrada
- [ ] Implementar CORS apropiadamente para tu dominio
- [ ] Usar gestión de secretos para datos sensibles
- [ ] Habilitar autenticación en MongoDB

## 📦 Dependencias

### Dependencias Principales
- **FastAPI**: Marco web
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validación de datos
- **Motor**: Controlador asincrónico de MongoDB
- **python-dotenv**: Gestión de variables de entorno

### Dependencias de Desarrollo
- **Pytest**: Marco de pruebas
- **pytest-asyncio**: Soporte para pruebas asincrónicas
- **Black**: Formateador de código
- **isort**: Ordenador de importaciones
- **mypy**: Verificador de tipos

Ver `pyproject.toml` para la lista completa de dependencias.

## 🚀 Despliegue en Producción

### Lista de Verificación Previa al Despliegue

- [ ] Establece `DEBUG=false` en el entorno
- [ ] Configura credenciales seguras de MongoDB
- [ ] Establece `CORS_ORIGINS` apropiadamente
- [ ] Configura `MONGODB_URL` con Atlas o base de datos de producción
- [ ] Habilita HTTPS/TLS
- [ ] Configura monitoreo y registro
- [ ] Configura copias de seguridad
- [ ] Ejecuta la suite completa de pruebas
- [ ] Realiza auditoría de seguridad

### Despliegue vía Docker

```bash
# Construir imagen de producción
docker build -t pdf-extractext:v1.0.0 .

# Empujar al registro
docker push your-registry/pdf-extractext:v1.0.0

# Desplegar con docker-compose
docker-compose -f docker-compose.yml up -d
```

### Despliegue en Kubernetes

Crea `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdf-extractext-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pdf-extractext-api
  template:
    metadata:
      labels:
        app: pdf-extractext-api
    spec:
      containers:
      - name: api
        image: your-registry/pdf-extractext:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 🐛 Solución de Problemas

### Error de Conexión a MongoDB

```bash
# Verifica si MongoDB está ejecutándose
# macOS
brew services list

# Windows
Get-Service MongoDB

# Docker
docker ps | grep mongodb
```

### Puerto ya en Uso

```bash
# Encuentra proceso usando puerto 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Finaliza proceso
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Errores de Importación

```bash
# Asegúrate de que el entorno virtual esté activado
# Reinstala el paquete en modo desarrollo
pip install -e .

# Limpia caché de Python
find . -type d -name __pycache__ -exec rm -r {} +
```

## 📚 Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Pydantic](https://docs.pydantic.dev/)
- [Documentación de Motor](https://motor.readthedocs.io/)
- [Documentación de MongoDB](https://docs.mongodb.com/)
- [Guía de Arquitectura Limpia](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver archivo LICENSE para más detalles.

## 👥 Contribuyendo

¡Las contribuciones son bienvenidas! Por favor sigue el flujo de trabajo de desarrollo y asegúrate de:

1. Todas las pruebas pasen
2. El código esté formateado con Black
3. Incluye anotaciones de tipos
4. La documentación esté actualizada

## 📞 Soporte

Para problemas, preguntas o sugerencias:

1. Consulta la sección de solución de problemas
2. Revisa la documentación de API en `/docs`
3. Abre un problema en GitHub
4. Contacta al equipo de desarrollo

---

**¡Feliz codificación! 🎉**
