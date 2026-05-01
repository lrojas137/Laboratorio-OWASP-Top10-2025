# Laboratorio OWASP Top 10:2025 - Aplicación Flask Vulnerable

Este repositorio contiene el desarrollo del laboratorio de seguridad de aplicaciones web basado en **OWASP Top 10:2025**. El objetivo fue analizar una aplicación vulnerable en Python/Flask, identificar riesgos de seguridad, aplicar correcciones y validar las mitigaciones mediante herramientas de análisis estático y dinámico.

## Objetivo del laboratorio

Identificar, analizar y mitigar vulnerabilidades de seguridad en una aplicación web mediante el uso de herramientas como **Bandit** y **OWASP ZAP**, aplicando buenas prácticas de codificación segura y configuración adecuada.

## Herramientas utilizadas

- Python
- Flask
- Visual Studio Code
- Git y GitHub
- Bandit
- OWASP ZAP
- pip-audit

## Actividades realizadas

Durante el laboratorio se desarrollaron las siguientes actividades:

1. Estudio de los principales riesgos de **OWASP Top 10:2025**.
2. Clonación de una aplicación vulnerable desarrollada en Python/Flask.
3. Configuración del entorno local de desarrollo.
4. Análisis estático del código fuente con **Bandit**.
5. Implementación de correcciones sobre los hallazgos identificados.
6. Despliegue local de la aplicación.
7. Pruebas dinámicas de seguridad con **OWASP ZAP**.
8. Documentación de hallazgos e identificación de riesgos.
9. Priorización de vulnerabilidades según OWASP Top 10:2025.
10. Aplicación de medidas de corrección y mitigación.

## Hallazgos identificados

### Análisis estático con Bandit

En el análisis inicial se identificaron vulnerabilidades relacionadas con:

- Posible SQL Injection.
- Ejecución de comandos del sistema con `shell=True`.
- Uso inseguro de `pickle.loads()`.
- Exposición del servicio en `0.0.0.0`.
- Uso de módulos potencialmente peligrosos como `subprocess`.

Después de aplicar las correcciones, se ejecutó nuevamente Bandit y no se identificaron issues pendientes en el archivo corregido.

### Análisis dinámico con OWASP ZAP

Inicialmente, OWASP ZAP identificó alertas relacionadas con:

- Falta de cabecera `Content-Security-Policy`.
- Falta de protección anti-clickjacking.
- Exposición de información del servidor en la cabecera `Server`.
- Falta de cabecera `X-Content-Type-Options`.

Después de aplicar las mitigaciones y ejecutar nuevamente el escaneo, no se presentaron alertas activas en OWASP ZAP.

## Correcciones aplicadas

Las principales correcciones implementadas fueron:

| Riesgo identificado | Corrección aplicada |
|---|---|
| SQL Injection | Se reemplazaron consultas construidas por cadenas por consultas parametrizadas. |
| Command Injection | Se eliminó el uso de `subprocess` con `shell=True`. |
| Deserialización insegura | Se reemplazó `pickle` por procesamiento de datos en formato JSON. |
| Exposición de servicio | Se cambió la ejecución de `0.0.0.0` a `127.0.0.1`. |
| Modo inseguro de ejecución | Se deshabilitó el modo debug. |
| Falta de cabeceras HTTP | Se agregaron cabeceras de seguridad mediante `@app.after_request`. |
| Exposición de versión del servidor | Se redujo la información técnica expuesta por Werkzeug. |

## Cabeceras de seguridad implementadas

Se agregaron cabeceras HTTP para fortalecer la seguridad de la aplicación:

- `Content-Security-Policy`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`

Estas cabeceras permiten mitigar riesgos como XSS, clickjacking, MIME sniffing y exposición innecesaria de información.

## Ejecución local de la aplicación

Para ejecutar la aplicación localmente, primero se debe crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Luego se instalan las dependencias:

```bash
pip install -r requirements.txt
```

Finalmente, se ejecuta la aplicación:

```bash
python vulnerable-flask-app-windows.py
```

La aplicación queda disponible en:

```text
http://127.0.0.1:8081/
```

## Validación con Bandit

Para ejecutar el análisis estático con Bandit:

```bash
bandit vulnerable-flask-app-windows.py -f txt -o reportes/bandit_reporte_corregido.txt
```

## Validación con OWASP ZAP

Para validar dinámicamente la aplicación:

1. Ejecutar la aplicación localmente.
2. Abrir OWASP ZAP.
3. Usar la opción **Automated Scan**.
4. Ingresar la URL:

```text
http://127.0.0.1:8081/
```

5. Revisar la sección **Alerts**.
6. Generar el reporte final del análisis.

## Estructura del repositorio

```text
Vulnerable-Flask-App/
│
├── vulnerable-flask-app-windows.py
├── vulnerable-flask-app-linux.py
├── requirements.txt
├── test.db
├── reportes/
│   ├── bandit_reporte.txt
│   ├── bandit_reporte_corregido.txt
│   └── reporte_zap.pdf
├── informe/
│   └── Informe_Laboratorio_OWASP_Top10_2025.pdf
├── README.md
└── .gitignore
```


