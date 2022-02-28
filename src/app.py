from flask import Flask, request, jsonify
from configparser import ConfigParser
import pathlib
import sqlite3
import json


app = Flask(__name__)
app.config["DEBUG"] = True
current_dir = pathlib.Path(__file__).parent
configs = ConfigParser()
configs.read(current_dir / "configs.properties")


def get_db(configs=configs, current_dir=current_dir):
    db = sqlite3.connect(current_dir / configs["general"]["users"])
    return db


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT contact, bus, school, always_notify FROM users;")
    user_list = cursor.fetchall()
    conn.close()
    return {
        "users": [
            {
                "contact": user[0],
                "bus": user[1],
                "school": user[2],
                "always_notify": user[3],
            }
            for user in user_list
        ],
        "status": 200,
    }


@app.route("/remove/<phone_num>", methods=["POST"])
def remove_user(phone_num):
    phone_number = "+1" + phone_num
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT contact, bus, school, always_notify FROM users WHERE contact = "{phone_number}"'
    )
    found_records = cursor.fetchall()
    if found_records:
        cursor.execute(f'DELETE FROM users WHERE contact = "{phone_number}";')
        conn.commit()
        conn.close()
        return {
            "removed_users": [
                {
                    "contact": user[0],
                    "bus": user[1],
                    "school": user[2],
                    "always_notify": user[3],
                }
                for user in found_records
            ],
            "status": 200,
        }


if __name__ == "__main__":
    app.run()
