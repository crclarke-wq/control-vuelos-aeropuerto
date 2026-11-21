

TARIFAS = {"E": 85000, "J": 210000, "P": 450000}
NOMBRES_CLASE = {"E": "Económica", "J": "Ejecutiva", "P": "Primera"}
TASA = 12500


def formato_precio(monto):
    return f"${monto:,}".replace(",", ".")


def mostrar_menu():
    print("\n===== AEROPUERTO INTERNACIONAL CORDILLERA =====")
    print("1. Registrar vuelo")
    print("2. Vender pasajes")
    print("3. Cambiar estado de vuelo")
    print("4. Mostrar vuelos")
    print("5. Reporte de la jornada")
    print("6. Salir")


def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo and numero <= maximo:
                return numero
            else:
                print(f"El número debe estar entre {minimo} y {maximo}")
        except ValueError:
            print("Debes ingresar un número entero")


def validar_codigo(codigo):
    if len(codigo) != 6:
        return False
    for i in range(6):
        caracter = codigo[i]
        if i < 2:
            if caracter < "A" or caracter > "Z":
                return False
        else:
            if caracter < "0" or caracter > "9":
                return False
    return True


def buscar_vuelo(vuelos, codigo):
    for vuelo in vuelos:
        if vuelo["codigo"] == codigo:
            return vuelo
    return None


def registrar_vuelo(vuelos):
    print("\n--- Registrar vuelo ---")
    codigo = input("Código del vuelo (ej: LA1234): ").strip()
    if not validar_codigo(codigo):
        print("El código debe tener 2 letras mayúsculas y 4 dígitos")
        return
    if buscar_vuelo(vuelos, codigo) is not None:
        print("Ya existe un vuelo con ese código")
        return
    destino = input("Destino: ").strip()
    if destino == "":
        print("El destino no puede quedar vacío")
        return
    capacidad = leer_entero("Capacidad (50 a 300): ", 50, 300)
    vuelos.append({
        "codigo": codigo,
        "destino": destino,
        "capacidad": capacidad,
        "vendidos": 0,
        "estado": "Programado",
        "recaudado": 0
    })
    print(f"Vuelo agregado: {codigo} - {destino}")


def asientos_disponibles(vuelo):
    return vuelo["capacidad"] - vuelo["vendidos"]


def calcular_ocupacion(vuelo):
    return round(vuelo["vendidos"] / vuelo["capacidad"] * 100, 1)


def calcular_total_venta(clase, cantidad):
    subtotal = TARIFAS[clase.upper()] * cantidad
    if cantidad >= 4:
        subtotal = subtotal - subtotal * 10 // 100
    return subtotal + TASA * cantidad


def vender_pasajes(vuelos):
    print("\n--- Vender pasajes ---")
    codigo = input("Código del vuelo: ").strip()
    vuelo = buscar_vuelo(vuelos, codigo)
    if vuelo is None:
        print("Este código no existe")
        return
    if vuelo["estado"] != "Programado" and vuelo["estado"] != "Embarcando":
        print(f"No se puede vender, el vuelo está {vuelo['estado']}")
        return
    disponibles = asientos_disponibles(vuelo)
    print(f"Asientos disponibles: {disponibles}")
    if disponibles == 0:
        print("El vuelo no tiene asientos disponibles")
        return
    clase = input("Clase (E=Económica, J=Ejecutiva, P=Primera): ").strip().upper()
    if clase not in TARIFAS:
        print("La clase debe ser E, J o P")
        return
    cantidad = leer_entero("Cantidad de pasajes (1 a 10): ", 1, 10)
    if cantidad > disponibles:
        print(f"Solo quedan {disponibles} asientos disponibles")
        return
    total = calcular_total_venta(clase, cantidad)
    print("\n--- Detalle de la venta ---")
    print(f"Vuelo: {vuelo['codigo']} - {vuelo['destino']}")
    print(f"Clase: {NOMBRES_CLASE[clase]} x {cantidad}")
    if cantidad >= 4:
        print("Descuento 10% aplicado sobre los pasajes")
    print(f"Tasa aeroportuaria: {formato_precio(TASA * cantidad)}")
    print(f"TOTAL A PAGAR: {formato_precio(total)}")
    vuelo["vendidos"] += cantidad
    vuelo["recaudado"] += total


def cambiar_estado(vuelos):
    print("\n--- Cambiar estado de vuelo ---")
    codigo = input("Código del vuelo: ").strip()
    vuelo = buscar_vuelo(vuelos, codigo)
    if vuelo is None:
        print("Este código no existe")
        return
    estado = vuelo["estado"]
    if estado == "Programado":
        opciones = ["Embarcando", "Cancelado"]
    elif estado == "Embarcando":
        opciones = ["Despegado", "Cancelado"]
    else:
        print(f"Un vuelo {estado} ya no puede cambiar de estado")
        return
    print(f"Estado actual: {estado}")
    for i, nuevo_estado in enumerate(opciones, 1):
        print(f"{i}. {nuevo_estado}")
    opcion = leer_entero("Seleccione el nuevo estado: ", 1, len(opciones))
    vuelo["estado"] = opciones[opcion - 1]
    print(f"El vuelo {codigo} ahora está {vuelo['estado']}")


def mostrar_vuelos(vuelos):
    print("\n--- Vuelos del día ---")
    print(f"{'Código':<8}{'Destino':<18}{'Vendidos':<11}{'Ocupación':<11}Estado")
    for vuelo in vuelos:
        vendidos = f"{vuelo['vendidos']}/{vuelo['capacidad']}"
        ocupacion = f"{calcular_ocupacion(vuelo)}%"
        print(f"{vuelo['codigo']:<8}{vuelo['destino']:<18}{vendidos:<11}{ocupacion:<11}{vuelo['estado']}")


def generar_reporte(vuelos):
    print("\n--- Reporte de la jornada ---")
    pasajeros_totales = 0
    total_recaudado = 0
    cancelados = 0
    mayor_ocupacion = vuelos[0]
    for vuelo in vuelos:
        pasajeros_totales += vuelo["vendidos"]
        total_recaudado += vuelo["recaudado"]
        if vuelo["estado"] == "Cancelado":
            cancelados += 1
        if calcular_ocupacion(vuelo) > calcular_ocupacion(mayor_ocupacion):
            mayor_ocupacion = vuelo
    print(f"Total de vuelos: {len(vuelos)}")
    print(f"Pasajeros totales: {pasajeros_totales}")
    print(f"Total recaudado del día: {formato_precio(total_recaudado)}")
    print(f"Vuelo con mayor ocupación: {mayor_ocupacion['codigo']} - {mayor_ocupacion['destino']} ({calcular_ocupacion(mayor_ocupacion)}%)")
    print(f"Vuelos cancelados: {cancelados}")


def main():
    vuelos = [
        {"codigo": "LA1234", "destino": "Lima", "capacidad": 180, "vendidos": 150, "estado": "Programado", "recaudado": 0},
        {"codigo": "JA0456", "destino": "Buenos Aires", "capacidad": 120, "vendidos": 118, "estado": "Embarcando", "recaudado": 0},
        {"codigo": "SK7890", "destino": "Punta Arenas", "capacidad": 90, "vendidos": 40, "estado": "Programado", "recaudado": 0},
    ]
    try:
        while True:
            mostrar_menu()
            opcion = leer_entero("Seleccione una opción: ", 1, 6)
            if opcion == 1:
                registrar_vuelo(vuelos)
            elif opcion == 2:
                vender_pasajes(vuelos)
            elif opcion == 3:
                cambiar_estado(vuelos)
            elif opcion == 4:
                mostrar_vuelos(vuelos)
            elif opcion == 5:
                generar_reporte(vuelos)
            else:
                break
    except (KeyboardInterrupt, EOFError):
        print()
    print("Gracias por usar el sistema, hasta luego")


main()