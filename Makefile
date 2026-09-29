WEB_DIR := dashboard/web
NODE_MODULES := $(WEB_DIR)/node_modules

.DEFAULT_GOAL := dev
.PHONY: dev build serve install stop clean competitors

$(NODE_MODULES): $(WEB_DIR)/package.json
	cd $(WEB_DIR) && npm install
	@touch $(NODE_MODULES)

install: $(NODE_MODULES)

## make dev — backend + hot-reload frontend, two processes, Ctrl+C stops both
dev: $(NODE_MODULES)
	@echo "Backend  -> http://127.0.0.1:8787"
	@echo "Frontend -> http://127.0.0.1:5173 (hot reload, proxies /api + /media to the backend)"
	@echo "Both are also reachable from other devices on your Wi-Fi (e.g. your phone) —"
	@echo "vite prints the exact Network URL below once it starts. Trusted home Wi-Fi only:"
	@echo "the dashboard has real publish/AWS-touching endpoints."
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

## make competitors — pull competitor posts via Business Discovery, transcribe their top reels, then write growth/topic-backlog.md
competitors:
	uv run scripts/scrape_competitors.py
	uv run scripts/transcribe_competitors.py
	uv run scripts/build_topic_backlog.py

## make stop — kill any leftover dashboard/vite processes
stop:
	@pkill -f "dashboard/server.py" 2>/dev/null || true
	@pkill -f "vite" 2>/dev/null || true
	@echo "stopped"

## make clean — remove installed deps + build output
clean:
	rm -rf $(NODE_MODULES) dashboard/static
