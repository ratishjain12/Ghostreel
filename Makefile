WEB_DIR := dashboard/web
NODE_MODULES := $(WEB_DIR)/node_modules

.DEFAULT_GOAL := dev
.PHONY: dev build serve install stop clean

$(NODE_MODULES): $(WEB_DIR)/package.json
	cd $(WEB_DIR) && npm install
	@touch $(NODE_MODULES)

install: $(NODE_MODULES)

## make dev — backend + hot-reload frontend, two processes, Ctrl+C stops both
dev: $(NODE_MODULES)
	@echo "Backend  -> http://127.0.0.1:8787"
	@echo "Frontend -> http://127.0.0.1:5173 (hot reload, proxies /api + /media to the backend)"
	@uv run dashboard/server.py & backend=$$!; \
	trap "kill $$backend 2>/dev/null" EXIT INT TERM; \
	cd $(WEB_DIR) && npm run dev; \
	kill $$backend 2>/dev/null

## make build — production frontend bundle into dashboard/static
build: $(NODE_MODULES)
	cd $(WEB_DIR) && npm run build

## make serve — build once, then single process on :8787 (no hot reload)
serve: build
	@echo "Dashboard -> http://127.0.0.1:8787"
	uv run dashboard/server.py

## make stop — kill any leftover dashboard/vite processes
stop:
	@pkill -f "dashboard/server.py" 2>/dev/null || true
	@pkill -f "vite" 2>/dev/null || true
	@echo "stopped"

## make clean — remove installed deps + build output
clean:
	rm -rf $(NODE_MODULES) dashboard/static
