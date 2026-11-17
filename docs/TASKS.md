# Tasks

## 0. Before you start

Check the Relate documentation (`docs/limitations.md` in its GitHub repository):

- [ ] What happens if two processes open the same `.rl` file?
- [ ] Is the entire graph loaded into RAM when it opens?
- [ ] Does the Python API provide `close()` and `flush()`?

## 1. Project setup

- [ ] Create the repository with `router/`, `worker/`, `firebase/`, and `data/` directories, and add `data/` to `.gitignore`
- [ ] Create a `docker-compose.yml` with the router, one worker, and the Firebase emulators
- [ ] Set up a container for the Firebase emulators (Firestore and Storage) that saves its data on shutdown

## 2. Worker

- [ ] Create a FastAPI app that runs as a single process (`uvicorn --workers 1`)
- [ ] Open and close graphs with `POST /internal/graphs/{id}/open` and `POST /internal/graphs/{id}/close`
- [ ] Run Cypher queries with `POST /internal/graphs/{id}/query`
- [ ] Automatically close idle graphs when memory runs low
- [ ] Add `GET /internal/stats` to report each graph's size and the container's memory usage

## 3. Router

- [ ] Create a FastAPI app with a public API to create, list, delete, and query graphs
- [ ] Store graph and worker records in Firestore (`graphs` and `workers` collections)
- [ ] Keep an in-memory copy of the catalog and update it automatically with `on_snapshot`
- [ ] Route each query to the worker that holds the graph
- [ ] Protect the API with an API key

## 4. Multiple workers

- [ ] Add a second worker pool
- [ ] Assign new graphs to the least-loaded worker
- [ ] Check every 30 seconds that the workers are still running

## 5. Backups and archiving

- [ ] Upload and download `.rl` files between the worker and Storage
- [ ] Add `POST /graphs/{id}/backup`
- [ ] Archive graphs in Storage after N days of inactivity
- [ ] Restore an archived graph when a query comes in

## 6. Move large graphs to dedicated containers

- [ ] Detect when a graph exceeds the size threshold
- [ ] Create the dedicated container from the router using the Docker SDK for Python
- [ ] Move the graph by closing it in the pool, opening it in the dedicated container, and updating the catalog
- [ ] If anything fails, move the graph back to the pool

## 7. Google Cloud

- [ ] Set up a Compute Engine VM with Docker and no public IP address
- [ ] Use Persistent Disk for `.rl` files and take daily snapshots
- [ ] Create a Cloud Storage bucket for backups and archived graphs
- [ ] Use Firestore in place of the emulator
- [ ] Push container images to Artifact Registry
- [ ] Connect your Cloud Run APIs to the VM over a private network
- [ ] Schedule daily backups with Cloud Scheduler and a Cloud Run job

## Later

- [ ] Sync data from Firestore to the graphs with a Cloud Function
- [ ] Move graphs that outgrow a single VM to Neo4j