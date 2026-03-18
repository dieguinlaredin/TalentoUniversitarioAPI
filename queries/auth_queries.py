from database.connection import get_connection


def crear_usuario(email: str, passwd: str) -> dict:
    connection = get_connection()
    if not connection:
        return {"ok": False, "error": "No se pudo conectar a la BD"}

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (email, passwd, rol_id)
            VALUES (%s, %s, %s)
            """,
            (email, passwd, "3"),
        )
        connection.commit()

        return {"ok": True, "usuario_id": cursor.lastrowid}

    except Exception as ex:
        try:
            connection.rollback()
        except Exception:
            pass
        print(f"Error al crear usuario: {ex}")
        return {"ok": False, "error": "Error al crear usuario"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
