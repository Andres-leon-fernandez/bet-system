# Bet System — Documentación del Backend

## 1. ¿Qué hace este sistema?

Es una plataforma de **simulación de apuestas deportivas** basada en datos históricos de los Mundiales de Fútbol (2002-2022).

El sistema puede:

- Analizar estadísticas históricas de equipos
- Calcular probabilidades con Machine Learning
- Generar cuotas (odds) a partir de probabilidades
- Permitir apuestas simuladas con saldo virtual
- Resolver automáticamente las apuestas cuando termina un partido
- Mostrar reportes y estadísticas

---

## 2. Stack tecnológico

| Tecnología | Para qué se usa |
|---|---|
| **Python 3.14** | Lenguaje principal |
| **FastAPI** | Framework web (API REST) |
| **Uvicorn** | Servidor ASGI para correr FastAPI |
| **SQLAlchemy** | ORM para base de datos |
| **SQLite** | Base de datos local (desarrollo) |
| **PostgreSQL (Neon)** | Base de datos en la nube (producción) |
| **Pandas** | Análisis y limpieza de datos |
| **NumPy** | Operaciones numéricas y simulación |
| **Scikit-learn** | Random Forest para predicciones |
| **Joblib** | Guardar/cargar modelos entrenados |
| **Pydantic** | Validación de datos (usado por FastAPI) |

---

## 3. Estructura del proyecto

```
Lenguajes-Programacion/          ← Raíz del repositorio (GitHub)
│
├── backend-bet/                 ← ★ Todo el backend está aquí
│   │
│   ├── main.py                  ← Punto de entrada (levanta FastAPI)
│   ├── requirements.txt         ← Dependencias del proyecto
│   ├── README.md                ← Descripción básica
│   ├── SYSTEM.md                ← ★ Este documento
│   │
│   ├── analytics/               ← Ciencia de datos
│   │   ├── exploracion.py       ←   Conocer el dataset
│   │   ├── limpieza.py          ←   Limpiar datos (nulos, duplicados)
│   │   ├── estadisticas.py      ←   Calcular estadísticas
│   │   ├── prediccion.py        ←   ★ Entrenar modelo ML
│   │   ├── cuotas.py            ←   Probabilidades → cuotas
│   │   └── simulacion.py        ←   Simular partidos (Poisson)
│   │
│   ├── domain/                  ← Clases del negocio (POO)
│   │   ├── equipo.py            ←   Equipo (nombre, continente, ranking)
│   │   ├── usuario.py           ←   Usuario (nombre, email, saldo)
│   │   ├── partido.py           ←   Partido (equipos, fecha, resultado)
│   │   ├── apuesta.py           ←   Apuesta (usuario, selección, monto)
│   │   ├── mercado.py           ←   Tipo de mercado (1X2, etc.)
│   │   ├── cuota.py             ←   Valor de cuota por selección
│   │   └── casa_apuestas.py     ←   (vacio - para futuro)
│   │
│   ├── logic/                   ← Reglas de negocio
│   │   ├── reglas.py            ←   Reglas (saldo, cuotas, límites)
│   │   ├── validaciones.py      ←   Validaciones (montos, estados)
│   │   └── motor.py             ←   ★ Orquestador (procesar, resolver)
│   │
│   ├── services/                ← Orquestación entre capas
│   │   ├── usuario_service.py   ←   CRUD + dominio de usuarios
│   │   ├── partido_service.py   ←   CRUD + dominio de partidos
│   │   ├── apuesta_service.py   ←   ★ Apostar, resolver, cancelar
│   │   ├── prediccion_service.py ←  ML + cuotas + simulación
│   │   └── reporte_service.py   ←   Estadísticas y reportes
│   │
│   ├── database/                ← Persistencia
│   │   ├── connection.py        ←   ★ Conexión a BD (Neon o SQLite)
│   │   ├── models.py            ←   ★ Modelos SQLAlchemy (tablas)
│   │   ├── usuario_repository.py ←  CRUD usuarios
│   │   ├── equipo_repository.py ←   CRUD equipos
│   │   ├── partido_repository.py ←  CRUD partidos
│   │   └── apuesta_repository.py ←  CRUD apuestas
│   │
│   ├── api/                     ← FastAPI endpoints
│   │   ├── usuarios.py          ←   /usuarios
│   │   ├── partidos.py          ←   /partidos
│   │   ├── apuestas.py          ←   /apuestas
│   │   ├── predicciones.py      ←   /predicciones
│   │   └── reportes.py          ←   /reportes
│   │
│   ├── datasets/                ← Datos históricos
│   │   └── worldcup.csv         ←   192 registros, 24 columnas
│   │
│   ├── models/                  ← Modelos entrenados
│   │   ├── modelo.pkl           ←   Random Forest entrenado
│   │   ├── scaler.pkl           ←   Escalador StandardScaler
│   │   └── features.pkl         ←   Lista de features usadas
│   │
│   └── doc/                     ← Documentación del dataset
│       ├── tabla.md             ←   Significado de cada columna
│       ├── pandas.md            ←   Comandos útiles de Pandas
│       └── preguntas-a-responder.md ← Preguntas del EDA
│
├── front-bet/                   ← Frontend React (vacío por ahora)
│
└── .gitignore                   ← Archivos ignorados por git
```

---

## 4. Arquitectura por capas

Cada carpeta responde una pregunta diferente y **no depende de las otras carpetas**:

```
┌─────────────────────────────────────────────────────────────┐
│                         api/                                │
│              FastAPI — solo recibe HTTP y responde JSON     │
│         No sabe de Pandas, no sabe de bases de datos        │
└──────────────────────────┬──────────────────────────────────┘
                           │ llama a
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       services/                             │
│          Orquestación — conecta todo sin conocer detalles   │
│     "Usuario quiere apostar" → valida → guarda → responde   │
└──────┬──────────────┬──────────────┬────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌──────────┐  ┌────────────┐  ┌──────────────┐
│ domain/  │  │  logic/    │  │  database/   │
│ Objetos  │  │  Reglas    │  │  Persistencia│
│ POO puro │  │  + Motor   │  │  SQLAlchemy  │
└──────────┘  └────────────┘  └──────────────┘
       │                            │
       └──────────┬─────────────────┘
                  ▼
         ┌────────────────┐
         │  analytics/    │
         │  Pandas + ML   │
         │  Solo datos    │
         └────────────────┘
```

### Regla de oro del proyecto

> **Cada capa debe poder funcionar sin las demás.**

Ejemplos:

- `analytics/` funciona aunque no exista FastAPI
- `domain/` se prueba sin base de datos
- `logic/` valida apuestas sin frontend
- `services/` coordina sin conocer SQL

---

## 5. Las clases del dominio (domain/)

Son objetos Python puros. **No usan Pandas, ni FastAPI, ni base de datos.**

### Equipo

```python
class Equipo:
    atributos: nombre, continente, ranking_fifa, valor_mercado
```

### Usuario

```python
class Usuario:
    atributos: nombre, email, saldo, historial_apuestas

    método tiene_saldo_suficiente(monto) → bool
    método descontar_saldo(monto)        → descuenta si alcanza
    método abonar_ganancia(monto)        → suma al saldo
```

### Partido

```python
class Partido:
    atributos: equipo_local, equipo_visitante, fecha, estado, goles

    estado puede ser: "pendiente", "en_curso", "finalizado"

    método iniciar()                      → cambia estado a "en_curso"
    método finalizar(goles_local, goles_visitante) → cambia a "finalizado"
    método resultado()                    → "local", "empate" o "visitante"
```

### Apuesta

```python
class Apuesta:
    atributos: usuario, partido, seleccion, cuota, monto, estado

    estado puede ser: "pendiente", "ganada", "perdida", "cancelada"

    método resolver(resultado_partido)    → cambia a ganada o perdida
    método cancelar()                     → cambia a cancelada
    método calcular_ganancia()            → monto * cuota
```

### Mercado

```python
class Mercado:
    atributos: nombre, descripcion
    # Ejemplo: "1X2" (local, empate, visitante)
```

### Cuota

```python
class Cuota:
    atributos: mercado, valor_local, valor_empate, valor_visitante

    método obtener_valor(seleccion) → float
```

---

## 6. Las reglas de negocio (logic/)

Son funciones. **No son clases.** Responden preguntas como:

```
¿Puede apostar?       → reglas.puede_apostar(usuario, monto)
¿Cuánto gana?         → reglas.calcular_ganancia(monto, cuota)
¿Es cuota válida?     → reglas.es_cuota_valida(cuota)
¿Está dentro límites? → reglas.esta_dentro_limites(monto)
```

### Límites definidos

| Concepto | Valor |
|---|---|
| Monto mínimo por apuesta | $1 |
| Monto máximo por apuesta | $10,000 |
| Cuota mínima | 1.01 |
| Cuota máxima | 1000.0 |

### validaciones.py

Valida que los datos sean correctos antes de hacer algo. Si algo falla, lanza `ErrorValidacion`:

```python
validar_monto(monto)        # → error si negativo o fuera de límites
validar_usuario(usuario)    # → error si es None
validar_partido(partido)    # → error si no existe o ya terminó
validar_seleccion(seleccion) # → error si no es local/empate/visitante
validar_cuota(cuota)        # → error si fuera del rango permitido

validar_apuesta(usuario, partido, monto, cuota, seleccion)
    → Ejecuta TODAS las validaciones de una vez
    → Si hay errores, los junta en un solo mensaje
```

### motor.py

Orquesta el flujo completo:

```python
procesar_apuesta(usuario, partido, seleccion, cuota, monto)
    1. Valida todo (llama a validar_apuesta)
    2. Verifica saldo suficiente
    3. Crea el objeto Apuesta
    4. Descuenta el saldo del usuario
    5. Registra en el historial
    → Devuelve la Apuesta

resolver_apuestas_partido(partido, lista_apuestas)
    1. Verifica que el partido esté finalizado
    2. Obtiene el resultado (local/empate/visitante)
    3. Por cada apuesta pendiente:
       - Si acertó → estado "ganada", abona ganancia
       - Si no → estado "perdida"
    → Devuelve lista de apuestas resueltas

cancelar_apuesta(apuesta)
    1. Verifica que esté pendiente
    2. Cambia estado a "cancelada"
    3. Reembolsa el monto al usuario
```

---

## 7. Base de datos (database/)

### Conexión

Usa SQLAlchemy. Puedes usar:

- **SQLite** (local) → por defecto, crea `bet_system.db`
- **PostgreSQL en Neon** → configura la variable de entorno:

```bash
# En Windows PowerShell:
$env:DATABASE_URL="postgresql://usuario:contraseña@ep-tu-proyecto.us-east-2.aws.neon.tech/bet_system?sslmode=require"

# En Git Bash / Linux:
export DATABASE_URL="postgresql://..."
```

Si no configuras la variable, usará SQLite automáticamente.

### Tablas

```text
┌───────────┐     ┌───────────┐     ┌───────────┐
│  usuarios │     │  equipos  │     │  partidos │
├───────────┤     ├───────────┤     ├───────────┤
│ id        │     │ id        │     │ id        │
│ nombre    │     │ nombre    │     │ local_id  │──→ equipos.id
│ email     │     │ continente│     │ visit_id  │──→ equipos.id
│ saldo     │     │ ranking   │     │ fecha     │
└─────┬─────┘     │ valor_mer │     │ estado    │
      │           └───────────┘     │ goles_l   │
      │                             │ goles_v   │
      │                             └──────┬─────┘
      │                                    │
      └──────────┐  ┌──────────────────────┘
                 ▼  ▼
          ┌──────────────┐
          │   apuestas   │
          ├──────────────┤
          │ id           │
          │ usuario_id   │──→ usuarios.id
          │ partido_id   │──→ partidos.id
          │ seleccion    │
          │ cuota        │
          │ monto        │
          │ estado       │
          │ ganancia_pot │
          │ ganancia_real│
          └──────────────┘
```

### Repositorios

Cada repositorio hace CRUD de su tabla:

```python
UsuarioRepository(session)
    .crear(nombre, email, saldo)          → UsuarioDB
    .obtener_por_id(id)                   → UsuarioDB | None
    .obtener_por_email(email)             → UsuarioDB | None
    .listar()                              → [UsuarioDB]
    .actualizar_saldo(id, nuevo_saldo)    → UsuarioDB | None
```

---

## 8. Analytics — Ciencia de Datos

### exploracion.py

Para conocer el dataset:

```python
from analytics.exploracion import *
df = cargar_datos()
info = exploracion_basica(df)     # forma, columnas, nulos, duplicados
contar_equipos_unicos(df)         # 62 equipos
contar_continentes(df)            # Europa 82, Africa 31, etc.
ediciones_mundial(df)             # [2002, 2006, 2010, 2014, 2018, 2022]
```

### limpieza.py

Para limpiar datos:

```python
from analytics.limpieza import *
df_limpio = limpiar(df)
# Imputa nulos con la mediana (32 valores faltantes en market_value)
# Elimina duplicados
# Convierte tipos
```

### estadisticas.py

Para analizar:

```python
from analytics.estadisticas import *
top_equipos_goles_anotados(df, 10)    # Quién hizo más goles
resumen_por_continente(df)             # Promedios por continente
correlaciones(df)                      # Matriz de correlación
```

### prediccion.py — Machine Learning

**¿Qué predice?**

Predice si un equipo llegará a **semifinales** (`semi_finalist`) basado en datos anteriores al torneo.

**Features (17):**

- goals_scored_last_4y, goals_received_last_4y
- wins_last_4y, losses_last_4y, draws_last_4y
- world_cup_titles_before
- squad_total_market_value_eur
- fifa_rank_pre_tournament, fifa_points_pre_tournament
- squad_avg_age
- world_cup_participations_before
- groups_passed_before, round16_before, quarterfinals_before
- semifinals_before, finals_before, is_host

**Modelo:** RandomForestClassifier con 200 árboles, max_depth=10

**Rendimiento:** 81.25% de precisión

**Cómo entrenar:**

```bash
python analytics/prediccion.py
```

Esto guarda `models/modelo.pkl`, `models/scaler.pkl` y `models/features.pkl`.

**Cómo usar el modelo:**

```python
from analytics.prediccion import predecir_probabilidades
probs = predecir_probabilidades(df)
# → DataFrame con team, version, probabilidad_semi_final
```

### cuotas.py

Convierte probabilidades en cuotas:

```python
from analytics.cuotas import *
generar_cuotas_1x2(0.55, 0.25, 0.20)
# → {'local': 1.91, 'empate': 4.21, 'visitante': 5.26}

generar_cuotas_desde_fuerza(70, 30)
# → probabilidades + cuotas basados en fuerza relativa
```

Aplica overround del 5% (margen de la casa).

### simulacion.py

Simula partidos usando distribución Poisson:

```python
from analytics.simulacion import *
simular_partido(1.8, 1.2)
# → {'goles_local': 2, 'goles_visitante': 1, 'resultado': 'local'}

simular_n_partidos(1.8, 1.2, 10000)
# → DataFrame con frecuencias de local/empate/visitante
```

---

## 9. Servicios (services/)

Conectan las capas. Son los "directores de orquesta".

### UsuarioService

```python
crear_usuario(nombre, email, saldo)      → dict con datos del usuario
obtener_usuario(id)                       → dict | None
listar_usuarios()                          → [dict]
obtener_dominio(id)                        → Usuario | None (objeto domain)
```

### PartidoService

```python
crear_partido(equipo_local, equipo_visitante, fecha) → dict
finalizar_partido(id, goles_local, goles_visitante)  → dict
obtener_partido(id)                                   → dict | None
obtener_dominio(id)                                   → Partido | None
listar_partidos()                                     → [dict]
```

### ApuestaService

```python
realizar_apuesta(usuario_id, partido_id, seleccion, cuota, monto)
    → dict con la apuesta creada

resolver_apuestas_partido(partido_id)
    → [dict] con resultados de cada apuesta

cancelar_apuesta(apuesta_id)
    → dict confirmando cancelación + reembolso

historial_usuario(usuario_id)
    → [dict] con todas las apuestas del usuario
```

### PrediccionService

```python
generar_cuotas_para_partido(fuerza_local, fuerza_visitante)
    → dict con probabilidades + cuotas

simular_partido(fuerza_local, fuerza_visitante, n=1000)
    → [dict] con frecuencias de resultados

predecir_partido(df_equipos)
    → [dict] con probabilidades de llegar a semifinal
```

### ReporteService

```python
resumen_apuestas()
    → dict con total, ganadas, perdidas, pendientes, total apostado

top_apostadores(limite=5)
    → [dict] con nombre, email, saldo

estadisticas_partidos()
    → dict con total, finalizados, pendientes
```

---

## 10. API — Endpoints FastAPI

| Método | Ruta | Parámetros | Respuesta |
|---|---|---|---|
| `GET` | `/` | — | `{"message": "Bet System API..."}` |
| `POST` | `/usuarios/` | nombre, email, saldo (opc) | Usuario creado |
| `GET` | `/usuarios/` | — | Lista de usuarios |
| `GET` | `/usuarios/{id}` | — | Usuario por ID |
| `POST` | `/partidos/` | equipo_local, equipo_visitante, fecha | Partido creado |
| `GET` | `/partidos/` | — | Lista de partidos |
| `GET` | `/partidos/{id}` | — | Partido por ID |
| `PUT` | `/partidos/{id}/finalizar` | goles_local, goles_visitante | Partido finalizado |
| `POST` | `/apuestas/` | usuario_id, partido_id, seleccion, cuota, monto | Apuesta creada |
| `POST` | `/apuestas/{id}/cancelar` | — | Apuesta cancelada |
| `GET` | `/apuestas/usuario/{id}` | — | Historial del usuario |
| `POST` | `/predicciones/cuotas` | fuerza_local, fuerza_visitante | Probabilidades + cuotas |
| `POST` | `/predicciones/simular` | fuerza_local, fuerza_visitante, n (opc) | Simulación |
| `GET` | `/reportes/apuestas` | — | Resumen de apuestas |
| `GET` | `/reportes/top-apostadores` | limite (opc) | Top apostadores |
| `GET` | `/reportes/partidos` | — | Estadísticas de partidos |

### Cómo probar la API

```bash
# 1. Iniciar el servidor
cd backend-bet
python -m uvicorn main:app --reload

# 2. Abrir en el navegador
# http://localhost:8000/docs      ← Documentación interactiva (Swagger)
# http://localhost:8000/redoc     ← Documentación alternativa

# 3. O con curl
curl http://localhost:8000/usuarios/
```

---

## 11. Cómo usar el sistema paso a paso

```
1. Iniciar servidor
   → python -m uvicorn main:app --reload

2. Crear equipos (directamente en BD o con script)
   → Desde Swagger no hay endpoint para crear equipos aún
   → Usar script: python -c "
       from database import init_db, get_session, EquipoRepository
       init_db()
       session = get_session()
       repo = EquipoRepository(session)
       repo.crear('Brasil', 'South America', 1)
       repo.crear('Argentina', 'South America', 2)
       session.close()
     "

3. Crear usuarios
   → POST /usuarios/  (nombre, email, saldo)

4. Crear partidos
   → POST /partidos/  (equipo_local, equipo_visitante, fecha)

5. Apostar
   → POST /apuestas/  (usuario_id, partido_id, seleccion, cuota, monto)

6. Finalizar partido
   → PUT /partidos/{id}/finalizar (goles_local, goles_visitante)

7. Ver resultados
   → GET /apuestas/usuario/{id}     ← Historial
   → GET /reportes/apuestas          ← Resumen global
```

---

## 12. Conexión a Neon (PostgreSQL en la nube)

```bash
# 1. Crear cuenta gratis en https://neon.tech
# 2. Crear un proyecto (te dan una URL como esta:)
#    postgresql://user:pass@ep-xxxx.us-east-2.aws.neon.tech/bet_system?sslmode=require

# 3. Configurar la variable de entorno
export DATABASE_URL="postgresql://user:pass@ep-xxxx.us-east-2.aws.neon.tech/bet_system?sslmode=require"

# 4. Iniciar el servidor (crea las tablas automáticamente)
python -m uvicorn main:app --reload
```

Si no configuras `DATABASE_URL`, usa SQLite automáticamente (se crea `bet_system.db`).

---

## 13. Cómo se guardan los modelos

Los modelos entrenados se guardan en `models/`:

```python
# Entrenar (desde analytics/prediccion.py)
modelo.fit(X_train, y_train)
joblib.dump(modelo, "models/modelo.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(features, "models/features.pkl")

# Cargar (desde analytics/prediccion.py)
modelo = joblib.load("models/modelo.pkl")
scaler = joblib.load("models/scaler.pkl")
features = joblib.load("models/features.pkl")
```

Para reentrenar:

```bash
python analytics/prediccion.py
```

---

## 14. Guía rápida para agregar funcionalidades

### Agregar un nuevo endpoint

```python
# 1. En api/foo.py
from fastapi import APIRouter
router = APIRouter(prefix="/foo", tags=["Foo"])

@router.get("/")
def mi_endpoint():
    return {"mensaje": "hola"}

# 2. En main.py
from api.foo import router as foo_router
app.include_router(foo_router)
```

### Agregar una nueva tabla

```python
# 1. En database/models.py
class FooDB(Base):
    __tablename__ = "foos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

# 2. En database/foo_repository.py
class FooRepository:
    def __init__(self, session): ...

# 3. En database/__init__.py
from .foo_repository import FooRepository
```

### Agregar una nueva regla de negocio

```python
# En logic/reglas.py o logic/validaciones.py
def nueva_regla(parametro) -> bool:
    return condicion
```

---

## 15. Comandos útiles

```bash
# Iniciar servidor
python -m uvicorn main:app --reload

# Entrenar modelo
python analytics/prediccion.py

# Probar análisis exploratorio
python analytics/exploracion.py

# Probar estadísticas
python analytics/estadisticas.py

# Probar cuotas
python analytics/cuotas.py

# Probar simulación
python analytics/simulacion.py

# Instalar dependencias
pip install -r requirements.txt
```

---

## 16. Posibles errores y soluciones

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'sqlalchemy'` | Faltan dependencias | `pip install -r requirements.txt` |
| `UNIQUE constraint failed` | Ya existe un registro con ese email/nombre | Usar otro email/nombre |
| `Modelo no encontrado` | No has entrenado el modelo | `python analytics/prediccion.py` |
| `Connection refused` | Neon no está accesible | Revisar DATABASE_URL o usar SQLite |
| `PermissionError: test_bet.db` | La BD está bloqueada | Cerrar la terminal anterior |

---

> **Documentación generada para que cualquier agente (incluyendo futuros asistentes de IA) pueda retomar el proyecto sin confusión.**
>
> Última actualización: Julio 2026
