import matplotlib.pyplot as plt
import pandas as pd
import solara
import datos


@solara.component
def ReporteMIS(conn, periodo):
    filas = datos.reportar(conn, periodo)
    tabla = pd.DataFrame(filas, columns=["Municipio", "Toneladas"])
    solara.DataFrame(tabla)
    fig, ax = plt.subplots(figsize=(5, 2.5))
    ax.barh(tabla["Municipio"], tabla["Toneladas"], color="#2a6fdb")
    ax.invert_yaxis()
    ax.set_xlabel("toneladas")
    ax.spines[["top", "right"]].set_visible(False)
    solara.FigureMatplotlib(fig)
    plt.close(fig)
