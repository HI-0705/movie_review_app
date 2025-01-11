import sys
import os
import sqlite3
from services.movie_api import get_subscription_providers


def resource_path(relative_path):
    """ﾘｿｰｽﾌｧｲﾙへのﾊﾟｽ"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


DB_PATH = resource_path(os.path.join("data", "database.db"))
SQL_PATH = resource_path(os.path.join("data", "schema.sql"))


def init_db():
    """ｽｷｰﾏ生成"""
    try:
        with sqlite3.connect(DB_PATH) as conn, open(SQL_PATH, "r") as f:
            conn.executescript(f.read())
    except sqlite3.Error as e:
        print(f"sqlite3.Error: {e}")
    except IOError as e:
        print(f"IOError: {e}")


def execute_query(query, params=()):
    """ｸｴﾘ実行"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    except sqlite3.Error as e:
        print(f"Error:execute_query")
        return None


def fetch_all(query, params=()):
    """ﾃﾞｰﾀﾍﾞｰｽから情報を取得"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"ﾃﾞｰﾀの取得に失敗しました")
        return []


def get_reviews():
    """ﾚﾋﾞｭｰﾃﾞｰﾀ取得"""
    query = "SELECT id, title, review, rating, created_at FROM reviews"
    return fetch_all(query)


def save_selected_subscriptions(provider_ids):
    """ｻﾌﾞｽｸ設定保存"""
    query_clear = "DELETE FROM subscriptions"
    execute_query(query_clear)

    query_insert = (
        "INSERT INTO subscriptions (provider_id, provider_name) VALUES (?, ?)"
    )
    providers = get_subscription_providers()
    provider_mapping = {p["id"]: p["name"] for p in providers}

    for provider_id in provider_ids:
        if provider_id in provider_mapping:
            execute_query(query_insert, (provider_id, provider_mapping[provider_id]))


def load_selected_subscriptions():
    """ｻﾌﾞｽｸ設定読込"""
    query = "SELECT provider_id FROM subscriptions"
    return [row[0] for row in fetch_all(query)]


def add_to_watchlist(movie_id, title):
    """ｳｫｯﾁﾘｽﾄ追加"""
    query = "INSERT INTO watchlist (id, title) VALUES (?, ?)"
    execute_query(query, (movie_id, title))


def get_watchlist():
    """ｳｫｯﾁﾘｽﾄ取得"""
    query = "SELECT id, title, added_at FROM watchlist ORDER BY added_at DESC"
    return fetch_all(query)


def remove_from_watchlist(movie_id):
    """ｳｫｯﾁﾘｽﾄ削除"""
    query = "DELETE FROM watchlist WHERE id = ?"
    execute_query(query, (movie_id,))
