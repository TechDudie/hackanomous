# Hackanomous

monorepo for hc's next YSWS: Hackanomous!

### development

bun and uv strongly recommended.<br> `bun i` to install frontend deps, `uv venv .venv` and **activate the venv**, `uv sync` to install backend deps.<br> HMR isn't a thing here; closest would be `bun vite build --watch` in one tab, and `uv run main.py --dev` in the other.

oh also you need `config.toml`. ask me for a development copy.<br> also generate a rsa keypair! windows `ssh-keygen -t rsa -b 4096` and enter through stuff, if you're on linux figure it out yourself.
