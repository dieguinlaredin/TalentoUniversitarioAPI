from database.connection import get_connection

def obtener_datos() -> list:
    connection = get_connection()
    if not connection:
        return []
    
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                i.nombre AS institucion,
                i.cct,
                i.ciudad,
                i.estado,
                c.nombre AS carrera,
                c.nivel,
                e.nombre AS nombre,
                e.promedio,
                e.tipo_periodo,
                e.periodo_numero,
                e.disponibilidad
            FROM instituciones i
            LEFT JOIN carreras c 
                ON i.institucion_id = c.institucion_id
            LEFT JOIN estudiantes e 
                ON i.institucion_id = e.institucion_id 
                AND c.carrera_id = e.carrera_id
            ORDER BY e.alumno_id
            """
        )

        rows = cursor.fetchall()

        estudiantes = []

        for row in rows:
            if row.get('nombre') is None:
                continue

            estudiante = {
                "institucion": row["institucion"],
                "cct": row["cct"],
                "ciudad": row["ciudad"],
                "estado": row["estado"],
                "carrera": row["carrera"],
                "nivel": row["nivel"],
                "nombre": row["nombre"],
                "promedio": float(row["promedio"]) if row["promedio"] is not None else None,
                "tipo_periodo": row["tipo_periodo"],
                "periodo_numero": row["periodo_numero"],
                "disponibilidad": bool(row["disponibilidad"])
            }

            estudiantes.append(estudiante)

        return estudiantes

    except Exception as ex:
        print(f'Error al obtener datos completos: {ex}')
        return []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()