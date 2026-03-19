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
            (email, passwd, 3),
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

def obtener_clientes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT usuario_id, email, rol_id
        FROM usuarios
        WHERE rol_id = 3
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def aprobar_estudiante_query(id):
    connection = get_connection()
    if not connection:
        return {"ok": False, "error": "No se pudo conectar a la BD"}

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE estudiantes
            SET estatus = 'aprobado'
            WHERE alumno_id = %s
        """, (id,))

        connection.commit()

        if cursor.rowcount == 0:
            return {"ok": False, "error": "No se encontró el estudiante"}

        return {"ok": True}

    except Exception as ex:
        connection.rollback()
        print(f"Error al aprobar estudiante: {ex}")
        return {"ok": False, "error": "Error al actualizar"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
    
def obtener_estudiantes_pendientes():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            e.alumno_id,
            e.nombre,
            e.promedio,
            e.tipo_periodo,
            e.periodo_numero,
            e.disponibilidad,
            i.nombre AS institucion,
            i.cct,
            i.ciudad,
            i.estado,
            c.nombre AS carrera,
            c.nivel
        FROM estudiantes e
        LEFT JOIN instituciones i ON e.institucion_id = i.institucion_id
        LEFT JOIN carreras c ON e.carrera_id = c.carrera_id
        WHERE e.estatus = 'pendiente'
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data