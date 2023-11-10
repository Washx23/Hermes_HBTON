from flask import request, jsonify
from router import router
from router.utils import get_connection

@router.route("/urls/save", methods=["POST"])
def save_videos():
    data = request.get_json()
    if not data.get("url"):
        return jsonify({"error": "url missing in json data"}), 400
    if not data.get("user_id"):
        return jsonify({"error": "user_id missing in json data"}), 400

    db = get_connection()
    cur = db.cursor()
    try:
        query = """
            INSERT INTO video (video_url, user_id)
            VALUES (%s, %s)
            RETURNING id;
        """
        cur.execute(query, (data["url"], data["user_id"]))
        video_id = cur.fetchone()[0]
        db.commit()
        return jsonify({"message": "Video saved successfully", "video_id": video_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()




# @router.route("/urls/save", methods=["POST"])
# def save_videos():
#     data = request.get_json()
    
#     if not data.get("url"):
#         return jsonify("url missing in json data"), 400
#     if not data.get("")
    
#     db = get_connection()
    
#     cur = db.cursor()
    
# #     query = """
# #       INSERT   INTO video (video_url)
# #         VALUES(%s)
# #     """
    
# #     cur.execute(query, (data.get("url"),))
    
# #     db.commit()
# #     cur.close()
# #     db.close()
# #     return jsonify("joya pibe")




#     query = """
#             INSERT INTO video (videdevolverá el ID de la fila que acabas de insertar
#     """o_url, user_id)
#             VALUES (%s, %s)
#             RETURNING id;  -- Esto 

    
#     try:
#         # Ejecutar la consulta con los parámetros
#         cur.execute(query, (video_url, user_id))

#         # Obtener el id de la fila insertada
#         inserted_id = cur.fetchone()[0]
#         db.commit()  # No olvides hacer commit para guardar los cambios en la base de datos

#         print(f"Video insertado con ID: {inserted_id}")

#     except Exception as e:
#         # En caso de error, hacer rollback
#         db.rollback()
#         print(f"Error al insertar el video: {e}")

#     finally:
#         # Cerrar el cursor y la conexión
#         cur.close()
#         db.close()

@router.route("/urls/load/<path:video_url>", methods=["GET"])
def load_videos(video_url):
    db = get_connection()
    
    try:
        with db.cursor() as cur:
            query = "SELECT id FROM video WHERE video_url = %s"
            cur.execute(query, (video_url,))
            video_id = cur.fetchone()
            if video_id:
                return jsonify({"id": video_id[0]})
            else:
                return jsonify({"error": "URL no encontrada"}), 404
    except psycopg2.Error as e:
        return jsonify({"error": "Hubo un problema al acceder a la base de datos: " + str(e)}), 500
    finally:
        db.close()