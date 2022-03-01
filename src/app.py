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


def log_query(cursor, query):
    print("[query]", query)
    cursor.execute(query)
    return cursor


def jsonify_user_entry(user):
    return {
        "contact": user[0],
        "bus": user[1],
        "school": user[2],
        "always_notify": user[3],
    }


def get_db(configs=configs, current_dir=current_dir):
    db = sqlite3.connect(current_dir / configs["general"]["users"])
    return db


@app.route("/all_entries", methods=["GET"])
def all_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor = log_query(cursor, "SELECT contact, bus, school, always_notify FROM users;")
    user_list = cursor.fetchall()
    conn.close()
    return {
        "entries": [jsonify_user_entry(user) for user in user_list],
        "status": 200,
    }


@app.route("/user/<phone_num>", methods=["GET"])
def user(phone_num):
    phone_number = "+1" + phone_num
    conn = get_db()
    cursor = conn.cursor()
    cursor = log_query(
        cursor,
        f"SELECT contact, bus, school, always_notify FROM users WHERE contact = '{phone_number}';",
    )
    user_list = cursor.fetchall()
    conn.close()
    return {
        "users": [jsonify_user_entry(user) for user in user_list],
        "status": 200,
    }


@app.route("/remove/<phone_num>", methods=["POST"])
def remove(phone_num):
    bus = request.args.get("bus", None)
    school = request.args.get("school", None)
    always_notify = request.args.get("always_notify", None)
    phone_number = "+1" + phone_num
    school = school.lower().replace("_", " ")
    bus = f" AND bus = '{bus}'" if bus else ""
    school = f" AND school = '{school}'" if school else ""
    always_notify = f" AND always_notify = '{always_notify}'" if always_notify else ""
    conn = get_db()
    cursor = conn.cursor()
    cursor = log_query(
        cursor,
        f"SELECT contact, bus, school, always_notify FROM users WHERE contact = '{phone_number}'"
        + bus
        + school
        + always_notify,
    )
    found_records = cursor.fetchall()
    if found_records:
        cursor = log_query(
            cursor,
            f"DELETE FROM users WHERE contact = '{phone_number}'"
            + bus
            + school
            + always_notify,
        )
        conn.commit()
    conn.close()
    return {
        "removed_users": [jsonify_user_entry(user) for user in found_records],
        "status": 200,
    }


@app.route("/add_entry/<phone_num>", methods=["POST"])
def add_entry(phone_num):
    bus = request.args.get("bus")
    school = request.args.get("school")
    always_notify = request.args.get("always_notify", "F")
    phone_number = "+1" + phone_num
    school = school.lower().replace("_", " ")
    conn = get_db()
    cursor = conn.cursor()
    if bus and school:
        cursor = log_query(
            cursor,
            f"INSERT INTO users (contact, bus, school, always_notify) VALUES ('{phone_number}', '{bus}', '{school}', '{always_notify}');",
        )
        conn.commit()
        conn.close()
        return {
            "added_user": jsonify_user_entry((phone_num, bus, school, always_notify)),
            "status": 200,
        }
    else:
        conn.close()
        return {
            "status": 400,
            "message": "/add_user requires both a 'bus' parameter and 'school' parameter.",
        }


if __name__ == "__main__":
    app.run()
