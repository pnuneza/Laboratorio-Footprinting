# scanner.py
import subprocess
import threading
from colorama import Fore, Style

# Importamos la función de limpieza desde nuestro propio módulo utils
from utils import extraer_subdominio

def matar_proceso(proceso, nombre_herramienta):
    """Detiene forzosamente una herramienta si excede el tiempo."""
    print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}[!] ¡TIEMPO LÍMITE ALCANZADO!{Fore.WHITE} Deteniendo '{nombre_herramienta}' de forma segura...")
    proceso.kill()

def ejecutar_herramienta(comando, dominio_objetivo, tiempo_limite):
    """Ejecuta el comando en terminal, controla el tiempo y retorna subdominios."""
    nombre_herramienta = comando[0]
    
    print(f"{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐")
    print(f"{Fore.MAGENTA}│ {Fore.CYAN}[*] INICIANDO: {Fore.WHITE}{' '.join(comando)}")
    print(f"{Fore.MAGENTA}│ {Fore.CYAN}[*] LÍMITE: {Fore.WHITE}{tiempo_limite}s {Fore.LIGHTBLACK_EX}| Presiona Ctrl+C para saltar")
    print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘\n")
    
    subdominios_herramienta = set()
    
    try:
        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        temporizador = threading.Timer(tiempo_limite, matar_proceso, args=[proceso, nombre_herramienta])
        temporizador.start()
        
        try:
            for linea in proceso.stdout:
                print(f"{Fore.LIGHTBLACK_EX}{linea}", end='')
                subdominio = extraer_subdominio(linea, dominio_objetivo)
                if subdominio:
                    subdominios_herramienta.add(subdominio)
            proceso.wait() 
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}{Style.BRIGHT}[!] Salto manual detectado (Ctrl+C).{Fore.WHITE} Deteniendo '{nombre_herramienta}' y rescatando datos...")
            proceso.kill()
            
        finally:
            temporizador.cancel()
            
        print(f"\n{Fore.GREEN}===============================================================")
        print(f"{Fore.GREEN}[✓] {nombre_herramienta.upper()} FINALIZADO. {Fore.WHITE}Rescató: {Style.BRIGHT}{len(subdominios_herramienta)} subdominios válidos.")
        print(f"{Fore.GREEN}===============================================================\n")
        
    except FileNotFoundError:
        print(f"\n{Fore.RED}[-] ERROR: La herramienta '{nombre_herramienta}' no está instalada.")
        print(f"{Fore.RED}    Prueba instalándola con: sudo apt install {nombre_herramienta}\n")
    except Exception as e:
        print(f"\n{Fore.RED}[-] Ocurrió un error inesperado al ejecutar '{nombre_herramienta}': {e}\n")
        
    return subdominios_herramienta