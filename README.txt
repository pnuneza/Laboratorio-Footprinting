Lenguaje usado: Python

=========================================================
ORQUESTADOR DE FOOTPRINTING Y CONSOLIDACIÓN (Versión Modular)
=========================================================

Este proyecto automatiza la ejecución de 5 herramientas modernas de footprinting 
instaladas en el sistema, captura sus salidas en tiempo real y utiliza 
la librería 'tldextract' combinada con expresiones regulares para limpiar 
formatos de consola, filtrar subdominios válidos, eliminar duplicados 
y ordenarlos alfabéticamente.

ARQUITECTURA MODULAR:
El código ha sido refactorizado aplicando el principio de "Separación de Preocupaciones" 
(Separation of Concerns), dividiendo el software en 4 módulos para mayor escalabilidad:
- main.py: Archivo principal y orquestador del flujo.
- ui.py: Manejo de la interfaz gráfica y arte ASCII en consola.
- utils.py: Funciones de limpieza, validación de red (DNS) y expresiones regulares.
- scanner.py: Motor de ejecución de subprocesos y control de temporizadores.

FUNCIONES AVANZADAS:
- Interfaz Premium: Diseño visual en consola estructurado y con colores (Colorama).
- Validación de Dominio: Verifica mediante DNS si el objetivo existe antes de iniciar.
- Análisis Cruzado: Identifica y reporta subdominios descubiertos por 2 o más herramientas.
- Temporizador: Limita cada herramienta a 3 minutos (180s) para evitar bloqueos de RAM.
- Salto Manual: Permite presionar 'Ctrl + C' para detener una herramienta lenta 
  y pasar a la siguiente sin perder los datos ya recolectados.

INSTRUCCIONES DE USO:

1. Requisitos del sistema:
   - Este script debe ejecutarse en un entorno Linux (ej. Kali Linux) 
     que tenga instaladas las siguientes herramientas:
     'subfinder', 'amass', 'findomain', 'dnsrecon' y 'gobuster'.
   - COMANDO DE INSTALACIÓN RÁPIDA: 
     sudo apt install subfinder findomain gobuster seclists -y

2. Crear y activar el Entorno Virtual (venv):
   - python3 -m venv venv
   - source venv/bin/activate

3. Instalar dependencias:
   - pip install -r requirements.txt

4. Ejecutar el script:
   - python3 main.py

El script pedirá un dominio objetivo (ej. trello.com), validará su existencia, 
ejecutará la orquestación en tiempo real y guardará el resultado consolidado 
en un archivo de texto limpio (ej. subdominios_trello.com.txt).