# utils.py
import re
import socket
import tldextract
from colorama import Fore, Style

def validar_dominio(dominio):
    """Verifica si el objetivo existe mediante DNS."""
    print(f"{Fore.CYAN}[*] {Fore.WHITE}Validando existencia del dominio {Style.BRIGHT}'{dominio}'{Style.NORMAL}...")
    
    extraccion = tldextract.extract(dominio)
    if not extraccion.domain or not extraccion.suffix:
        print(f"{Fore.RED}[-] Error: El formato es incorrecto. Debe ser algo como 'ejemplo.com'.")
        return False

    try:
        ip = socket.gethostbyname(dominio)
        print(f"{Fore.GREEN}[+] ¡Dominio válido y activo! Resolvió a la IP: {Style.BRIGHT}{ip}\n")
        return True
    except socket.gaierror:
        print(f"{Fore.RED}[-] Error: El dominio no existe o no tiene registros públicos en internet.")
        return False

def extraer_subdominio(linea, dominio_objetivo):
    """Limpia colores de consola y extrae el subdominio válido."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    linea_sin_color = ansi_escape.sub('', linea)
    linea_limpia = linea_sin_color.strip().lower()
    
    if not linea_limpia:
        return None

    extraccion = tldextract.extract(linea_limpia)
    
    if extraccion.domain and extraccion.suffix:
        dominio_base = f"{extraccion.domain}.{extraccion.suffix}"
        if dominio_base == dominio_objetivo:
            return extraccion.fqdn
            
    return None