#!/bin/bash
# Instalar navegadores de Playwright antes de arrancar Gunicorn
playwright install chromium
exec gunicorn proxy_pro:app --bind 0.0.0.0:$PORT
