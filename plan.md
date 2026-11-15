# Tareas
 
## 0. Antes de empezar
 
Revisar en la documentación de Relate (`docs/limitations.md` en su GitHub):
 
- [ ] ¿Qué pasa si dos procesos abren el mismo `.rl`?
- [ ] ¿El grafo completo se carga en RAM al abrirlo?
- [ ] ¿La API de Python tiene `close()` y `flush()`?
## 1. Base del proyecto
 
- [ ] Crear el repo con las carpetas `router/`, `worker/`, `firebase/` y `data/` (esta última en `.gitignore`)
- [ ] `docker-compose.yml` con router, un worker y los emuladores de Firebase
- [ ] Contenedor de emuladores de Firebase (Firestore + Storage) que guarde sus datos al apagarse
## 2. Worker
 
- [ ] App FastAPI con un solo proceso (`uvicorn --workers 1`)
- [ ] Abrir y cerrar grafos: `POST /internal/graphs/{id}/open` y `/close`
- [ ] Ejecutar Cypher: `POST /internal/graphs/{id}/query`
- [ ] Cerrar automáticamente los grafos que no se usan cuando se acaba la memoria
- [ ] `GET /internal/stats` con el tamaño de cada grafo y la memoria del contenedor
## 3. Router
 
- [ ] App FastAPI con la API pública: crear, listar, borrar y consultar grafos
- [ ] Guardar los grafos y workers en Firestore (colecciones `graphs` y `workers`)
- [ ] Copia del catálogo en memoria que se actualiza sola con `on_snapshot`
- [ ] Mandar cada consulta al worker que tiene el grafo
- [ ] API key para proteger la API
## 4. Varios workers
 
- [ ] Agregar un segundo worker pool
- [ ] Asignar los grafos nuevos al worker con menos carga
- [ ] Revisar cada 30 s que los workers sigan vivos
## 5. Backups y archivado
 
- [ ] Subir y bajar archivos `.rl` a Storage desde el worker
- [ ] `POST /graphs/{id}/backup`
- [ ] Archivar en Storage los grafos que no se usan en N días
- [ ] Reactivar un grafo archivado cuando llega una consulta
## 6. Mover grafos grandes a su propio contenedor
 
- [ ] Detectar cuando un grafo pasa el tamaño límite
- [ ] Crear el contenedor dedicado desde el router (Docker SDK de Python)
- [ ] Mover el grafo: cerrar en el pool → abrir en el dedicado → actualizar el catálogo
- [ ] Si algo falla, regresar el grafo al pool
## 7. Google Cloud
 
- [ ] VM de Compute Engine con Docker, sin IP pública
- [ ] Persistent Disk para los `.rl`, con snapshots diarios
- [ ] Bucket de Cloud Storage para backups y archivados
- [ ] Firestore real en lugar del emulador
- [ ] Subir las imágenes a Artifact Registry
- [ ] Conectar tus APIs de Cloud Run a la VM por red privada
- [ ] Backup diario con Cloud Scheduler + Cloud Run Job
## Después
 
- [ ] Sincronizar datos de Firestore a los grafos con una Cloud Function
- [ ] Mover a Neo4j los grafos que ya no quepan en una VM
 