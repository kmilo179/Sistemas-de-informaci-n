import solara
import datos

campos = {"cod_mpio": solara.reactive("15001"), "periodo": solara.reactive("2026-03"),
          "material": solara.reactive("vidrio"), "toneladas": solara.reactive("")}
mensaje = solara.reactive("")


def procesar(conn, valores):
    """Valida y registra. Devuelve 'Registrado...' o 'Rechazado...'."""
    if any(str(x).strip() == "" for x in valores.values()):
        return "Rechazado: hay campos vacíos"
    try:
        toneladas = float(valores["toneladas"])
    except ValueError:
        return "Rechazado: toneladas debe ser un número"
    ok = datos.registrar(conn, valores["cod_mpio"], valores["periodo"], valores["material"], toneladas)
    return "Registrado" if ok else "Rechazado por la base (municipio inexistente o toneladas <= 0)"


@solara.component
def Registro(conn):
    for nombre, estado in campos.items():
        solara.InputText(nombre, value=estado)
    def guardar():
        mensaje.set(procesar(conn, {k: e.value for k, e in campos.items()}))
    solara.Button("Guardar", on_click=guardar, color="primary")
    solara.Markdown(mensaje.value)
