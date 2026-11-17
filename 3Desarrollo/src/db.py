import sqlite3
from pathlib import Path
from src.auth import EQUIPO_CYBERANTS
from src.hormigas import Hormiga, HLarva, crear_alimento, reconstruir_hormiga

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "cyberants.db"


class CyberAntsDB:
    """Capa de persistencia SQLite alineada con el Modelo Entidad-Relación (MER)."""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS USUARIO (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    cedula TEXT NOT NULL,
                    nombre_completo TEXT NOT NULL,
                    rol_xp TEXT NOT NULL,
                    rol_hormiguero TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS HORMIGA (
                    id_hormiga INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL,
                    sexo TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS HISTORIAL_ALIMENTACION (
                    id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_hormiga INTEGER NOT NULL,
                    alimento TEXT NOT NULL,
                    tipo_resultante TEXT NOT NULL,
                    estado_resultante TEXT NOT NULL,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_hormiga) REFERENCES HORMIGA(id_hormiga)
                );
                """
            )

            # Sembrar integrantes del equipo si está vacío
            cur = conn.execute("SELECT COUNT(*) AS total FROM USUARIO")
            if cur.fetchone()["total"] == 0:
                for m in EQUIPO_CYBERANTS:
                    conn.execute(
                        """
                        INSERT INTO USUARIO (username, cedula, nombre_completo, rol_xp, rol_hormiguero)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (m.username, m.cedula, m.nombre, m.rol_xp, m.rol_hormiguero),
                    )

            # Sembrar 2 larvas iniciales si la tabla HORMIGA está vacía
            cur_h = conn.execute("SELECT COUNT(*) AS total FROM HORMIGA")
            if cur_h.fetchone()["total"] == 0:
                conn.execute(
                    "INSERT INTO HORMIGA (tipo, sexo, estado) VALUES ('HLarva', 'Asexual', 'VIVA')"
                )
                conn.execute(
                    "INSERT INTO HORMIGA (tipo, sexo, estado) VALUES ('HLarva', 'Asexual', 'VIVA')"
                )

    def listar_hormigas(self) -> list[Hormiga]:
        with self._connect() as conn:
            filas = conn.execute(
                "SELECT id_hormiga, tipo, sexo, estado FROM HORMIGA ORDER BY id_hormiga ASC"
            ).fetchall()
        return [
            reconstruir_hormiga(
                id=f["id_hormiga"],
                tipo=f["tipo"],
                sexo=f["sexo"],
                estado=f["estado"],
            )
            for f in filas
        ]

    def crear_hormiga(self, sexo: str = "Asexual") -> HLarva:
        sexo_limpio = (sexo or "Asexual").strip() or "Asexual"
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO HORMIGA (tipo, sexo, estado) VALUES ('HLarva', ?, 'VIVA')",
                (sexo_limpio,),
            )
            nuevo_id = cur.lastrowid
        return HLarva(id=nuevo_id, sexo=sexo_limpio, estado="VIVA")

    def alimentar_hormiga(self, id_hormiga: int, nombre_alimento: str) -> dict:
        alimento = crear_alimento(nombre_alimento)
        with self._connect() as conn:
            fila = conn.execute(
                "SELECT id_hormiga, tipo, sexo, estado FROM HORMIGA WHERE id_hormiga = ?",
                (id_hormiga,),
            ).fetchone()
            if fila is None:
                raise KeyError(f"No existe la hormiga con ID {id_hormiga}")

            hormiga = reconstruir_hormiga(
                id=fila["id_hormiga"],
                tipo=fila["tipo"],
                sexo=fila["sexo"],
                estado=fila["estado"],
            )
            tipo_anterior = hormiga.tipo
            sobrevive = hormiga.comer(alimento)

            conn.execute(
                "UPDATE HORMIGA SET tipo = ?, sexo = ?, estado = ? WHERE id_hormiga = ?",
                (hormiga.tipo, hormiga.sexo, hormiga.estado, id_hormiga),
            )
            conn.execute(
                """
                INSERT INTO HISTORIAL_ALIMENTACION
                (id_hormiga, alimento, tipo_resultante, estado_resultante)
                VALUES (?, ?, ?, ?)
                """,
                (id_hormiga, alimento.toString(), hormiga.tipo, hormiga.estado),
            )

        return {
            "hormiga": hormiga,
            "alimento": alimento.toString(),
            "tipo_anterior": tipo_anterior,
            "tipo_nuevo": hormiga.tipo,
            "sobrevive": sobrevive,
            "toString": hormiga.toString(),
        }

    def listar_historial(self, limite: int = 12) -> list[dict]:
        with self._connect() as conn:
            filas = conn.execute(
                """
                SELECT id_historial, id_hormiga, alimento, tipo_resultante, estado_resultante, fecha
                FROM HISTORIAL_ALIMENTACION
                ORDER BY id_historial DESC
                LIMIT ?
                """,
                (limite,),
            ).fetchall()
        return [dict(f) for f in filas]

    def reiniciar_hormiguero(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM HISTORIAL_ALIMENTACION")
            conn.execute("DELETE FROM HORMIGA")
            conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('HORMIGA', 'HISTORIAL_ALIMENTACION')")
        self.init_db()
