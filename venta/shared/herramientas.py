
import os

# Colores para la terminal
RESET = "\033[0m"
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MORADO = "\033[95m"
CYAN = "\033[96m"
BLANCO = "\033[97m"
NEGRITA = "\033[1m"


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_titulo(texto):
    print(f"\n{CYAN}{NEGRITA}")
    print("=" * 45)
    print(f"       {texto.upper()}")
    print("=" * 45)
    print(RESET)


def imprimir_exito(texto):
    print(f"{VERDE}[OK] {texto}{RESET}")


def imprimir_error(texto):
    print(f"{ROJO}[ERROR] {texto}{RESET}")


def imprimir_info(texto):
    print(f"{AZUL}[INFO] {texto}{RESET}")


def imprimir_opcion(numero, texto):
    print(f"{AMARILLO} [{numero}] {BLANCO}{texto}{RESET}")


def pausa():
    input(f"\n{CYAN}Presione Enter para continuar...{RESET}")


def confirmar(texto):
    respuesta = input(f"{AMARILLO}{texto} (s/n): {RESET}")
    return respuesta.strip().lower() in ("s", "si", "sí", "y", "yes")

