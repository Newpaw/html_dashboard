# Použijeme oficiální uv image s Pythonem 3.11 (slim verzi pro menší image).
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Ujistíme se, že uv instaluje balíčky do systémového prostředí kontejneru.
ENV UV_SYSTEM_PYTHON=1

# Zkopírujeme soubory s konfigurací závislostí: pyproject.toml a uv.lock.
COPY pyproject.toml uv.lock ./

# Nainstalujeme závislosti na základě uv.lock.
RUN uv sync --locked --no-install-project --no-cache --compile-bytecode

# Zkopírujeme zbytek souborů aplikace do kontejneru
COPY . .

# Vytvoříme složku pro nahrané soubory a nastavíme správná oprávnění.
RUN mkdir -p uploaded_files && chmod 777 uploaded_files

# Vystavíme port, na kterém Flask aplikace běží (výchozí je 5000).
EXPOSE 5000

# Spustíme aplikaci pomocí Python modulu gunicorn.
# TOTO JE KLÍČOVÁ ZMĚNA PRO OPRAVU "gunicorn not found".
CMD ["uv", "run", "python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]