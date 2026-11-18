import sys
import time
from pathlib import Path
from src.auth import AuthService
from src.contracts import Utility
from src.dron import AntCiberDron
from src.sistema_ruso import SistemaRuso

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "data" / "Grupo02.csv"


def generar_reporte_consola(csv_path: str | Path = DEFAULT_CSV) -> str:
    """Genera el reporte estándar de consola del sistema táctico KGD."""
    auth = AuthService()
    sistema = SistemaRuso()
    dron = AntCiberDron()
    coordenadas = sistema.readCoord(csv_path)

    lineas = [
        auth.formatear_ficha_equipo(),
        "",
        "[+] COORDENADAS UCRANIANAS:",
        "Loading | Geoposición | Lunes  | Martes | Miércoles | Jueves | Viernes | Tipo Arsenal",
    ]
    for c in coordenadas:
        lineas.append(c.to_console_line())

    lineas.append("")
    lineas.append("COORDENADAS UCRANIANAS A DESTRUIR:")
    lineas.append("Geoposición | Tipo Arsenal | Acción")
    for r in dron.evaluar_coordenadas(coordenadas):
        if r["accion"]:
            lineas.append(
                f"{r['geoposicion']:<11} | {r['tipoArsenal']:<12} | {r['accion_str']}"
            )
    return "\n".join(lineas)


def ejecutar_consola_interactiva(csv_path: str | Path = DEFAULT_CSV, delay: float = 0.04) -> None:
    """Ejecución en terminal con login de 3 intentos y animación \\ | / - 100%."""
    auth = AuthService()
    print("=== SISTEMA TÁCTICO KGD :: PROYECTO ANTDRON ===")
    while not auth.bloqueado and not auth.usuario_autenticado:
        try:
            usuario = input("Usuario: ")
            password = input("Contraseña: ")
        except EOFError:
            return
        res = auth.autenticar(usuario, password)
        if not res["exito"]:
            print(f"[!] {res['mensaje']}")

    if auth.bloqueado:
        return

    print()
    print(auth.formatear_ficha_equipo())
    print("\n[+] COORDENADAS UCRANIANAS:")
    print("Loading | Geoposición | Lunes  | Martes | Miércoles | Jueves | Viernes | Tipo Arsenal")

    sistema = SistemaRuso()
    coordenadas = sistema.readCoord(csv_path)
    for c in coordenadas:
        for paso in Utility.generar_pasos_loading():
            sys.stdout.write(f"\r{paso:<7}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(f"\r{c.to_console_line()}\n")
        sys.stdout.flush()

    dron = AntCiberDron()
    print("\nCOORDENADAS UCRANIANAS A DESTRUIR:")
    print("Geoposición | Tipo Arsenal | Acción")
    for r in dron.evaluar_coordenadas(coordenadas):
        if r["accion"]:
            print(f"{r['geoposicion']:<11} | {r['tipoArsenal']:<12} | {r['accion_str']}")


if __name__ == "__main__":
    ejecutar_consola_interactiva()
