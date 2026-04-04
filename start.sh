#!/bin/bash
# Arrancar Gunicorn directamente (ya no necesitas instalar navegadores de Playwright)
exec gunicorn proxy_pro:app --bind 0.0.0.0:$PORT --workers 1
