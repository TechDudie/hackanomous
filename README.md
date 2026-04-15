# Hackanomous

monorepo for hc's next YSWS: Hackanomous!

### development

bun and uv strongly recommended. `bun i` to install frontend deps, `uv venv .venv` and **activate the venv**, `uv sync` to install backend deps. HMR isn't a thing here; closest would be `bun vite build --watch` in one tab, and `uv run main.py --dev` in the other.