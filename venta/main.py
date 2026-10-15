
import os

from views import (
    ProductoController,
    VentaController,
    InventarioController,
    ClienteController,
    ProveedorController,
    CompraController,
)


# ==========================================
# COLORES
# ==========================================

RESET = "\033[0m"
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
MORADO = "\033[95m"
CYAN = "\033[96m"
BLANCO = "\033[97m"
NEGRITA = "\033[1m"


# ==========================================
# FUNCIONES GENERALES
# ==========================================

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input(f"\n{CYAN}Presione Enter para continuar...{RESET}")


def titulo(texto):
    print(f"\n{CYAN}{NEGRITA}")
    print("=" * 50)
    print(f"       {texto.upper()}")
    print("=" * 50)
    print(RESET)


def mensaje_error(texto):
    print(f"{ROJO}[ERROR] {texto}{RESET}")


def mensaje_exito(texto):
    print(f"{VERDE}[OK] {texto}{RESET}")


def etiqueta(campo):
    nombres = {
        "id": "ID",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "descripcion": "Descripción",
        "precio": "Precio",
        "stock": "Stock",
        "stock_minimo": "Stock mínimo",
        "cliente_id": "Cliente ID",
        "producto_id": "Producto ID",
        "proveedor_id": "Proveedor ID",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio unitario",
        "costo_unitario": "Costo unitario",
        "fecha": "Fecha",
        "telefono": "Teléfono",
        "email": "Correo electrónico",
        "direccion": "Dirección",
        "tipo_movimiento": "Tipo de movimiento",
        "detalle": "Detalle",
    }

    if campo in nombres:
        return nombres[campo]

    return campo.replace("_", " ").capitalize()


def normalizar_dato(modelo, campo, valor):
    """Acepta coma decimal en los campos numéricos decimales."""
    if campo in getattr(modelo, "NUMERICOS", ()):
        return str(valor).strip().replace(",", ".")

    return str(valor).strip()


def leer_id():
    valor = input(f"{AMARILLO}Ingrese el ID: {RESET}").strip()

    try:
        return int(valor)
    except ValueError:
        mensaje_error("El ID debe ser un número entero.")
        return None


# ==========================================
# MOSTRAR REGISTROS EN FORMA DE LISTA
# ==========================================

def mostrar_registros(registros, nombre):
    if not registros:
        print(f"{AMARILLO}No hay {nombre} registrados.{RESET}")
        return

    titulo(f"LISTA DE {nombre}")

    for numero, objeto in enumerate(registros, start=1):
        print(f"{MORADO}{NEGRITA}REGISTRO {numero}{RESET}")
        print(f"{AZUL}" + "-" * 40 + RESET)

        datos = objeto.a_diccionario()

        for campo, valor in datos.items():
            nombre_campo = etiqueta(campo)

            if campo == "precio" or campo == "precio_unitario":
                try:
                    valor = f"${float(valor):.2f}"
                except (ValueError, TypeError):
                    pass

            elif campo == "costo_unitario":
                try:
                    valor = f"${float(valor):.2f}"
                except (ValueError, TypeError):
                    pass

            print(
                f"{CYAN}{nombre_campo}:{RESET} "
                f"{BLANCO}{valor}{RESET}"
            )

        print(f"{AZUL}" + "-" * 40 + RESET)

    print(
        f"\n{VERDE}Total de registros: {len(registros)}{RESET}"
    )


# ==========================================
# CREAR REGISTRO
# ==========================================

def crear_registro(controlador):
    modelo = controlador.MODELO
    datos = {}

    titulo(f"CREAR {controlador.NOMBRE}")

    print(f"{CYAN}Complete los siguientes datos:{RESET}\n")

    for campo in modelo.CAMPOS:
        valor = input(
            f"{AMARILLO}{etiqueta(campo)}: {RESET}"
        ).strip()

        datos[campo] = normalizar_dato(modelo, campo, valor)

    exito, mensaje = controlador.crear(datos)

    if exito:
        mensaje_exito(mensaje)
    else:
        mensaje_error(mensaje)


# ==========================================
# LISTAR REGISTROS
# ==========================================

def listar_registros(controlador):
    registros = controlador.listar()
    mostrar_registros(registros, controlador.NOMBRE + "S")


# ==========================================
# BUSCAR REGISTRO
# ==========================================

def buscar_registro(controlador):
    titulo(f"BUSCAR {controlador.NOMBRE}")

    termino = input(
        f"{AMARILLO}Ingrese nombre, ID o dato para buscar: {RESET}"
    ).strip()

    resultados = controlador.buscar(termino)

    if resultados:
        mostrar_registros(resultados, "RESULTADOS")
    else:
        mensaje_error("No se encontraron registros.")


# ==========================================
# ACTUALIZAR REGISTRO
# ==========================================

def actualizar_registro(controlador):
    titulo(f"ACTUALIZAR {controlador.NOMBRE}")

    id_registro = leer_id()

    if id_registro is None:
        return

    objeto = controlador.obtener(id_registro)

    if objeto is None:
        mensaje_error("No se encontró el registro.")
        return

    datos_actuales = objeto.a_diccionario()
    cambios = {}

    print(f"\n{CYAN}Deje vacío un campo para conservar su valor.{RESET}\n")

    for campo in controlador.MODELO.CAMPOS:
        valor_actual = datos_actuales.get(campo, "")

        nuevo_valor = input(
            f"{AMARILLO}{etiqueta(campo)} "
            f"[{valor_actual}]: {RESET}"
        ).strip()

        if nuevo_valor:
            cambios[campo] = normalizar_dato(
                controlador.MODELO,
                campo,
                nuevo_valor
            )

    if not cambios:
        print(f"{AMARILLO}No se realizaron cambios.{RESET}")
        return

    exito, mensaje = controlador.actualizar(
        id_registro,
        cambios
    )

    if exito:
        mensaje_exito(mensaje)
    else:
        mensaje_error(mensaje)


# ==========================================
# ELIMINAR REGISTRO
# ==========================================

def eliminar_registro(controlador):
    titulo(f"ELIMINAR {controlador.NOMBRE}")

    id_registro = leer_id()

    if id_registro is None:
        return

    objeto = controlador.obtener(id_registro)

    if objeto is None:
        mensaje_error("No se encontró el registro.")
        return

    print(f"\n{AMARILLO}Registro seleccionado:{RESET}")
    mostrar_registros([objeto], controlador.NOMBRE)

    respuesta = input(
        f"\n{ROJO}¿Está seguro de eliminarlo? (s/n): {RESET}"
    ).strip().lower()

    if respuesta not in ("s", "si", "sí"):
        print(f"{CYAN}Operación cancelada.{RESET}")
        return

    exito, mensaje = controlador.eliminar(id_registro)

    if exito:
        mensaje_exito(mensaje)
    else:
        mensaje_error(mensaje)


# ==========================================
# MENÚ DE CADA MÓDULO
# ==========================================

def menu_modulo(nombre, controlador):
    while True:
        limpiar_pantalla()
        titulo(f"MÓDULO DE {nombre}")

        print(f"{VERDE}  [1] Crear registro{RESET}")
        print(f"{VERDE}  [2] Ver lista de registros{RESET}")
        print(f"{VERDE}  [3] Buscar registro{RESET}")
        print(f"{AMARILLO}  [4] Actualizar registro{RESET}")
        print(f"{ROJO}  [5] Eliminar registro{RESET}")
        print(f"{CYAN}  [0] Volver al menú principal{RESET}")

        print(f"\n{AZUL}" + "-" * 50 + RESET)

        opcion = input(
            f"{AMARILLO}Seleccione una opción: {RESET}"
        ).strip()

        try:
            if opcion == "1":
                crear_registro(controlador)

            elif opcion == "2":
                listar_registros(controlador)

            elif opcion == "3":
                buscar_registro(controlador)

            elif opcion == "4":
                actualizar_registro(controlador)

            elif opcion == "5":
                eliminar_registro(controlador)

            elif opcion == "0":
                break

            else:
                mensaje_error("Seleccione una opción válida.")

        except Exception as error:
            mensaje_error(f"Ocurrió un problema: {error}")

        if opcion != "0":
            pausa()


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def main():
    modulos = {
        "1": ("PRODUCTOS", ProductoController()),
        "2": ("VENTAS", VentaController()),
        "3": ("INVENTARIO", InventarioController()),
        "4": ("CLIENTES", ClienteController()),
        "5": ("PROVEEDORES", ProveedorController()),
        "6": ("COMPRAS", CompraController()),
    }

    while True:
        limpiar_pantalla()
        titulo("SISTEMA DE VENTAS")

        print(f"{VERDE}  [1] Productos{RESET}")
        print(f"{VERDE}  [2] Ventas{RESET}")
        print(f"{VERDE}  [3] Inventario{RESET}")
        print(f"{VERDE}  [4] Clientes{RESET}")
        print(f"{VERDE}  [5] Proveedores{RESET}")
        print(f"{VERDE}  [6] Compras{RESET}")
        print(f"{ROJO}  [0] Salir{RESET}")

        print(f"\n{AZUL}" + "-" * 50 + RESET)

        opcion = input(
            f"{AMARILLO}Seleccione una opción: {RESET}"
        ).strip()

        if opcion == "0":
            limpiar_pantalla()
            print(f"{VERDE}{NEGRITA}")
            print("=" * 50)
            print("   GRACIAS POR UTILIZAR EL SISTEMA")
            print("=" * 50)
            print(RESET)
            break

        if opcion in modulos:
            nombre, controlador = modulos[opcion]
            menu_modulo(nombre, controlador)
        else:
            mensaje_error("Seleccione una opción válida.")
            pausa()


if __name__ == "__main__":
    main()
