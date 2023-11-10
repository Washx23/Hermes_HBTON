from flask import request, jsonify
from router import router
from router.utils import get_connection

# @router.route("/", methods=["POST"])
# def create_user():

#     data = request.get_json()

#     if not data.get("email"):
#         return jsonify("email missing in json data"), 400
#     if not data.get("name"):
#         return jsonify("name missing in json data"), 400

#     db = get_connection()
    
#     cur = db.cursor()

#     query = """
#         INSERT INTO user_basics (name_inc, email)
#         VALUES (%s, %s)
#     """

#     cur.execute(query, (data.get("name"), data.get("email")))

#     db.commit()

#     cur.close()
#     db.close()
#     return jsonify("todo bien")

@router.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email"):
        return jsonify({"error": "email missing in json data"}), 400
    if not data.get("name"):
        return jsonify({"error": "name missing in json data"}), 400

    db = get_connection()
    cur = db.cursor()
    try:
        query = """
            INSERT INTO user_basics (name_inc, email)
            VALUES (%s, %s)
            RETURNING id;
        """
        cur.execute(query, (data["name"], data["email"]))
        user_id = cur.fetchone()[0]
        db.commit()
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        db.close()
