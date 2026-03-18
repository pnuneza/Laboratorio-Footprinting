# ui.py
from colorama import init, Fore, Style

# Inicializamos colorama
init(autoreset=True)

def imprimir_banner():
    """Imprime el logotipo ASCII al iniciar la herramienta."""
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
    ╔════════════════════════════════════════════════════════════╗
    ║  ███████╗██████╗  ██████╗ ████████╗                        ║
    ║  ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝  {Fore.WHITE}ORQUESTADOR OSINT{Fore.CYAN}     ║
    ║  █████╗  ██████╔╝██║   ██║   ██║     {Fore.WHITE}Y FOOTPRINTING{Fore.CYAN}        ║
    ║  ██╔══╝  ██╔══██╗██║   ██║   ██║                           ║
    ║  ██║     ██║  ██║╚██████╔╝   ██║     {Fore.LIGHTBLACK_EX}v2.0 - Modular Build{Fore.CYAN}  ║
    ║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝                           ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)