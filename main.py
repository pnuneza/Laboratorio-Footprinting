# main.py
import sys
from collections import Counter
from colorama import init, Fore, Style

# Importamos nuestros propios módulos locales
from ui import imprimir_banner
from utils import validar_dominio
from scanner import ejecutar_herramienta

init(autoreset=True)

def main():
    imprimir_banner()
    
    dominio = input(f"{Fore.YELLOW}[>] Ingrese el dominio objetivo (ej. trello.com): {Fore.WHITE}").strip().lower()
    print("")
    
    if not dominio or not validar_dominio(dominio):
        sys.exit(1)

    TIEMPO_LIMITE_SEGUNDOS = 180 

    comandos_a_ejecutar = [
        ["subfinder", "-d", dominio, "-silent"], 
        ["findomain", "-t", dominio, "-q"],
        ["amass", "enum", "-passive", "-d", dominio],
        ["dnsrecon", "-d", dominio, "-t", "std"],
        ["gobuster", "dns", "--domain", dominio, "-w", "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt", "-q"] 
    ]

    resultados_por_herramienta = {}

    for comando in comandos_a_ejecutar:
        nombre = comando[0]
        resultados_por_herramienta[nombre] = ejecutar_herramienta(comando, dominio, TIEMPO_LIMITE_SEGUNDOS)

    # ---------------- REPORTE FINAL ----------------
    print(f"{Fore.CYAN}{Style.BRIGHT}\n[*] {'='*15} REPORTE DETALLADO {'='*15}")
    
    todas_las_apariciones = [] 
    subdominios_unicos = set() 
    
    for nombre, subdominios in resultados_por_herramienta.items():
        print(f"\n{Fore.BLUE}[+] Herramienta: {nombre.upper()} {Fore.WHITE}({len(subdominios)} hallazgos)")
        if subdominios:
            for sub in sorted(subdominios):
                print(f"    {Fore.LIGHTBLACK_EX}└─ {Fore.WHITE}{sub}")
        else:
            print(f"    {Fore.RED}└─ (Ningún subdominio o proceso fallido)")
            
        todas_las_apariciones.extend(subdominios)
        subdominios_unicos.update(subdominios)

    frecuencia = Counter(todas_las_apariciones)
    subdominios_compartidos = {sub: count for sub, count in frecuencia.items() if count >= 2}
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[*] {'='*13} SUBDOMINIOS COMPARTIDOS {'='*13}")
    if subdominios_compartidos:
        print(f"{Fore.YELLOW}[!] Se detectaron {len(subdominios_compartidos)} subdominios confirmados por múltiples fuentes:")
        for sub, count in sorted(subdominios_compartidos.items(), key=lambda x: x[1], reverse=True):
            print(f"    {Fore.LIGHTBLACK_EX}└─ {Fore.WHITE}{sub} {Fore.YELLOW}(x{count})")
    else:
        print(f"    {Fore.LIGHTBLACK_EX}└─ (No hubo superposición de datos)")

    # ---------------- ESCRITURA DE ARCHIVO ----------------
    print(f"\n{Fore.CYAN}{Style.BRIGHT}[*] {'='*14} CONSOLIDACIÓN FINAL {'='*14}")
    
    if not subdominios_unicos:
        print(f"{Fore.RED}[-] Finalizado. No se encontraron subdominios válidos en total.")
        sys.exit(1)

    lista_ordenada = sorted(subdominios_unicos) 
    archivo_salida = f"subdominios_{dominio}.txt"

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for sub in lista_ordenada:
            f.write(f"{sub}\n")

    print(f"{Fore.GREEN}[+] ¡Orquestación completada con éxito!")
    print(f"{Fore.GREEN}[+] Total de subdominios únicos: {Style.BRIGHT}{len(lista_ordenada)}")
    print(f"{Fore.GREEN}[+] Archivo generado: {Style.BRIGHT}{Fore.WHITE}{archivo_salida}\n")

if __name__ == "__main__":
    main()