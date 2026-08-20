import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- ESTRUCTURAS DE DATOS BASE ---
# Tupla: Catálogo inicial inmutable
CATALOGO = ("P01", "P02", "P03", "P04", "P05")

# Diccionarios: Precios unitarios y Stock
PRECIOS = {"P01": 15.0, "P02": 25.0, "P03": 10.0, "P04": 50.0, "P05": 5.0}

STOCK = {"P01": 50, "P02": 30, "P03": 100, "P04": 20, "P05": 200}

# Lista: Buffer temporal en memoria para registrar ventas
buffer_ventas = []

# Archivos de persistencia
CSV_FILE = "ventas.csv"
LOG_FILE = "log.txt"


# --- FUNCIONES Y MODULARIDAD ---


def registrar_log(mensaje):
    """Escribe eventos y errores en log.txt (Manejo de archivos)."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{mensaje}\n")


def inicializar_csv():
    """Crea ventas.csv con 10 registros iniciales si el archivo no existe."""
    if not os.path.exists(CSV_FILE):
        ventas_base = [
            {
                "ID": "P01",
                "Cantidad": 2,
                "Precio_Unitario": 15.0,
                "Descuento": 0.0,
                "Total": 30.0,
            },
            {
                "ID": "P02",
                "Cantidad": 1,
                "Precio_Unitario": 25.0,
                "Descuento": 0.0,
                "Total": 25.0,
            },
            {
                "ID": "P03",
                "Cantidad": 10,
                "Precio_Unitario": 10.0,
                "Descuento": 0.05,
                "Total": 95.0,
            },
            {
                "ID": "P04",
                "Cantidad": 1,
                "Precio_Unitario": 50.0,
                "Descuento": 0.0,
                "Total": 50.0,
            },
            {
                "ID": "P05",
                "Cantidad": 12,
                "Precio_Unitario": 5.0,
                "Descuento": 0.05,
                "Total": 57.0,
            },
            {
                "ID": "P01",
                "Cantidad": 5,
                "Precio_Unitario": 15.0,
                "Descuento": 0.0,
                "Total": 75.0,
            },
            {
                "ID": "P02",
                "Cantidad": 10,
                "Precio_Unitario": 25.0,
                "Descuento": 0.05,
                "Total": 237.5,
            },
            {
                "ID": "P03",
                "Cantidad": 3,
                "Precio_Unitario": 10.0,
                "Descuento": 0.0,
                "Total": 30.0,
            },
            {
                "ID": "P04",
                "Cantidad": 2,
                "Precio_Unitario": 50.0,
                "Descuento": 0.0,
                "Total": 100.0,
            },
            {
                "ID": "P05",
                "Cantidad": 20,
                "Precio_Unitario": 5.0,
                "Descuento": 0.05,
                "Total": 95.0,
            },
        ]
        df_init = pd.DataFrame(ventas_base)
        df_init.to_csv(CSV_FILE, index=False)
        registrar_log(
            "SISTEMA: Creado ventas.csv inicial con 10 ventas registradas."
        )


def registrar_venta():
    """Registra venta con descuento (Reto C) y log de error si ID no existe (Reto D)."""
    print("\n--- REGISTRAR VENTA ---")
    p_id = input("Ingrese ID del producto (ej: P01): ").strip().upper()

    # Reto D: Validación de ID y escritura de intento fallido en log.txt
    if p_id not in CATALOGO:
        err_msg = (
            f"ERROR: Intento fallido de venta. ID '{p_id}' no está en el catálogo."
        )
        print(err_msg)
        registrar_log(err_msg)
        return

    try:
        cantidad = int(
            input(
                f"Ingrese cantidad a comprar (Stock actual de {p_id}: {STOCK[p_id]}): "
            )
        )

        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor a cero.")
            return

        if cantidad > STOCK[p_id]:
            print(
                f"Error: Stock insuficiente. Solo hay {STOCK[p_id]} disponibles."
            )
            return

        precio_unitario = PRECIOS[p_id]

        # Reto C: Aplicar 5% de descuento si cantidad >= 10
        if cantidad >= 10:
            descuento = 0.05
            print(">> ¡Se ha aplicado un 5% de descuento por volumen!")
        else:
            descuento = 0.0

        subtotal = cantidad * precio_unitario
        total = subtotal * (1 - descuento)

        # Actualización de estado
        STOCK[p_id] -= cantidad
        buffer_ventas.append(
            {
                "ID": p_id,
                "Cantidad": cantidad,
                "Precio_Unitario": precio_unitario,
                "Descuento": descuento,
                "Total": total,
            }
        )

        print(
            f"Venta registrada. Total a pagar: ${total:.2f} (Quedan {STOCK[p_id]} u. en stock)"
        )
        registrar_log(f"VENTA: {p_id} x{cantidad} u. Total: ${total:.2f}")

    except ValueError:
        print("Error: Ingrese un valor numérico entero.")
        registrar_log("ERROR: Entrada no válida en cantidad de venta.")


def guardar_ventas_csv():
    """Exporta el buffer de ventas temporal hacia ventas.csv con Pandas."""
    if not buffer_ventas:
        print("No hay ventas en memoria para guardar.")
        return

    try:
        df_nuevas = pd.DataFrame(buffer_ventas)
        header_necesario = not os.path.exists(CSV_FILE)
        df_nuevas.to_csv(CSV_FILE, mode="a", index=False, header=header_necesario)

        print(f"Éxito: Se guardaron {len(buffer_ventas)} registros en {CSV_FILE}.")
        buffer_ventas.clear()
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")
        registrar_log(f"ERROR CSV: {e}")


def analizar_metricas_numpy():
    """Lee el CSV con Pandas y calcula estadísticas avanzadas con NumPy."""
    print("\n--- ANÁLISIS DE MÉTRICAS (NumPy) ---")
    try:
        if not os.path.exists(CSV_FILE):
            raise FileNotFoundError(f"El archivo {CSV_FILE} no existe.")

        df = pd.read_csv(CSV_FILE)

        if df.empty:
            print("El archivo CSV está vacío.")
            return

        totales = df["Total"].to_numpy()
        n_registros = len(totales)

        # Cálculo de promedio seguro (División por cero controlada)
        promedio = np.divide(
            np.sum(totales),
            n_registros,
            out=np.array([0.0]),
            where=n_registros != 0,
        )[0]

        suma_total = np.sum(totales)
        desviacion_std = np.std(totales)

        print(f"Total de registros:       {n_registros}")
        print(f"Ingresos Totales (Sum):   ${suma_total:.2f}")
        print(f"Promedio por Venta (Mean):${promedio:.2f}")
        print(f"Desviación Estándar (Std):${desviacion_std:.2f}")

    except FileNotFoundError as err:
        print(f"Error de lectura: {err}")
        registrar_log(f"EXCEPCIÓN: {err}")
    except Exception as e:
        print(f"Error inesperado al analizar datos: {e}")


def graficar_ingresos(guardar_png=False):
    """Genera gráfica de barras con Matplotlib y exportación a PNG (Reto B)."""
    try:
        if not os.path.exists(CSV_FILE):
            print("No existe el archivo CSV para generar la gráfica.")
            return

        df = pd.read_csv(CSV_FILE)

        if df.empty:
            print("No hay datos en el CSV para graficar.")
            return

        ingresos_prod = df.groupby("ID")["Total"].sum()

        plt.figure(figsize=(8, 5))
        barras = plt.bar(
            ingresos_prod.index,
            ingresos_prod.values,
            color="skyblue",
            edgecolor="black",
        )

        plt.title("Ingresos Totales por Producto", fontsize=14, fontweight="bold")
        plt.xlabel("ID Producto", fontsize=12)
        plt.ylabel("Ingresos ($)", fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        for b in barras:
            h = b.get_height()
            plt.text(
                b.get_x() + b.get_width() / 2,
                h + 1,
                f"${h:.1f}",
                ha="center",
                va="bottom",
            )

        # Reto B: Exportar gráfico a PNG
        if guardar_png:
            plt.savefig("ingresos.png", dpi=300, bbox_inches="tight")
            print("Gráfico exportado exitosamente como 'ingresos.png'.")
            registrar_log("GRÁFICO: Exportado ingresos.png a disco.")

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error al generar gráfica: {e}")


def agregar_producto_nuevo():
    """Reto A: Modifica la Tupla del catálogo y actualiza Diccionarios."""
    global CATALOGO
    print("\n--- AGREGAR PRODUCTO AL CATÁLOGO (Reto A) ---")
    nuevo_id = input("Ingrese el nuevo ID (ej: P06): ").strip().upper()

    if nuevo_id in CATALOGO:
        print("El producto ya existe en el catálogo.")
        return

    try:
        precio = float(input(f"Ingrese precio para {nuevo_id}: "))
        stock = int(input(f"Ingrese stock para {nuevo_id}: "))

        if precio <= 0 or stock < 0:
            print("Precio o stock inválidos.")
            return

        # Modificación de tupla por reasignación
        CATALOGO = CATALOGO + (nuevo_id,)
        PRECIOS[nuevo_id] = precio
        STOCK[nuevo_id] = stock

        print(f"Producto '{nuevo_id}' agregado correctamente.")
        print(f"Catálogo Actualizado: {CATALOGO}")
        registrar_log(
            f"CATÁLOGO: Nuevo producto {nuevo_id} (Precio: ${precio}, Stock: {stock})"
        )

    except ValueError:
        print("Error: Ingrese valores numéricos válidos.")


# --- BUCLE PRINCIPAL DE NAVEGACIÓN ---
def menu():
    inicializar_csv()

    while True:
        print("\n" + "=" * 40)
        print("      MINITIENDA UIDE - MENÚ")
        print("=" * 40)
        print("1) Registrar venta")
        print("2) Guardar ventas en CSV")
        print("3) Analizar métricas (NumPy)")
        print("4) Graficar ingresos por producto")
        print("5) Agregar producto nuevo (Reto A)")
        print("6) Exportar gráfico a PNG (Reto B)")
        print("7) Salir")
        print("=" * 40)

        opcion = input("Seleccione una opción (1-7): ").strip()

        try:
            if opcion == "1":
                registrar_venta()
            elif opcion == "2":
                guardar_ventas_csv()
            elif opcion == "3":
                analizar_metricas_numpy()
            elif opcion == "4":
                graficar_ingresos(guardar_png=False)
            elif opcion == "5":
                agregar_producto_nuevo()
            elif opcion == "6":
                graficar_ingresos(guardar_png=True)
            elif opcion == "7":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
                continue

        except Exception as e:
            print(f"Error no esperado en menú: {e}")
        else:
            pass
        finally:
            pass


if __name__ == "__main__":
    menu()