import mysql.connector
from config import DB_CONFIG

def get_connection():
    """Establece la conexión con la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)

def guardar_pensamiento(persona: str, contenido: str, etiquetas_str: str):
    """
    Maneja la lógica transaccional completa:
    1. Busca o crea la Persona.
    2. Inserta el pensamiento (Información).
    3. Busca o crea los Temas.
    4. Vincula Información con Temas en la tabla puente.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # --- 1. GESTIONAR PERSONA ---
        # Verificamos si la persona ya existe
        cursor.execute("SELECT id FROM personas WHERE nombre = %s", (persona,))
        res = cursor.fetchone()
        
        if res:
            persona_id = res[0]
        else:
            # Si no existe, la creamos
            cursor.execute("INSERT INTO personas (nombre) VALUES (%s)", (persona,))
            persona_id = cursor.lastrowid

        # --- 2. INSERTAR INFORMACIÓN ---
        cursor.execute(
            "INSERT INTO informacion (persona_id, contenido) VALUES (%s, %s)", 
            (persona_id, contenido)
        )
        info_id = cursor.lastrowid

        # --- 3. GESTIONAR TEMAS (ETIQUETAS) ---
        if etiquetas_str:
            # Separamos por comas y limpiamos espacios
            lista_temas = [t.strip().lower() for t in etiquetas_str.split(',')]
            
            for tema in lista_temas:
                if not tema: continue # Saltar vacíos
                
                # Buscar si el tema ya existe
                cursor.execute("SELECT id FROM temas WHERE nombre_tema = %s", (tema,))
                res_tema = cursor.fetchone()
                
                if res_tema:
                    tema_id = res_tema[0]
                else:
                    # Crear nuevo tema
                    cursor.execute("INSERT INTO temas (nombre_tema) VALUES (%s)", (tema,))
                    tema_id = cursor.lastrowid
                
                # --- 4. CREAR VÍNCULO (Relación Muchos a Muchos) ---
                # Insertamos en la tabla puente 'info_temas'
                try:
                    cursor.execute(
                        "INSERT INTO info_temas (informacion_id, tema_id) VALUES (%s, %s)", 
                        (info_id, tema_id)
                    )
                except mysql.connector.errors.IntegrityError:
                    # Si ya existe la relación (raro en insert nuevo, pero posible), la ignoramos
                    pass

        conn.commit()
        return True, "Pensamiento guardado correctamente."

    except Exception as e:
        conn.rollback() # Si algo falla, deshacemos todo para no dejar datos corruptos
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def buscar_por_tema(tema: str):
    """Devuelve todas las notas asociadas a un tema (búsqueda parcial)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Query con JOINs para traer Nombre, Contenido y Temas
    query = """
        SELECT p.nombre, i.contenido 
        FROM informacion i
        JOIN personas p ON i.persona_id = p.id
        JOIN info_temas it ON i.id = it.informacion_id
        JOIN temas t ON it.tema_id = t.id
        WHERE t.nombre_tema LIKE %s
        ORDER BY i.fecha_registro DESC
    """
    cursor.execute(query, (f"%{tema}%",))
    resultados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return resultados

def obtener_perfil(nombre: str):
    """Devuelve toda la información de una persona específica."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Usamos GROUP_CONCAT para unir todos los temas de una nota en una sola celda
    query = """
        SELECT i.contenido, GROUP_CONCAT(t.nombre_tema SEPARATOR ', ') as temas
        FROM informacion i
        JOIN personas p ON i.persona_id = p.id
        LEFT JOIN info_temas it ON i.id = it.informacion_id
        LEFT JOIN temas t ON it.tema_id = t.id
        WHERE p.nombre LIKE %s
        GROUP BY i.id
        ORDER BY i.fecha_registro DESC
    """
    cursor.execute(query, (f"%{nombre}%",))
    resultados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return resultados