import os
import requests

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")  # 環境変数からAPIｷｰを取得


def make_request(url, params=None):
    """ﾘｸｴｽﾄ送信"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"APIﾘｸｴｽﾄに失敗しました: {e}")
        return {}


def get_movies_genre_list():
    """ｼﾞｬﾝﾙ取得"""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": "ja-JP"}
    data = make_request(url, params)
    return [
        {"name": genre.get("name", "不明"), "id": genre.get("id")}
        for genre in data.get("genres", [])
    ]


def search_movies(query):
    """映画名検索"""
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query, "language": "ja-JP"}
    results = make_request(url, params)
    return results.get("results", [])


def get_subscription_providers():
    """ﾌﾟﾛﾊﾞｲﾀﾞID取得"""
    url = "https://api.themoviedb.org/3/watch/providers/movie"
    params = {"api_key": TMDB_API_KEY, "language": "ja-JP", "watch_region": "JP"}
    data = make_request(url, params)
    return [
        {
            "name": provider.get("provider_name", "不明"),
            "id": provider.get("provider_id"),
        }
        for provider in data.get("results", [])
    ]


def search_movies_by_filters(genre=None, year=None, subscriptions=None):
    """条件検索"""
    if not subscriptions:
        return []

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {"api_key": TMDB_API_KEY, "language": "ja-JP"}
    if genre:
        params["with_genres"] = genre
    if year:
        params["primary_release_year"] = year

    # ﾌﾟﾛﾊﾞｲﾀﾞ別にﾘｸｴｽﾄ
    all_results = []
    for provider in subscriptions:
        provider_params = {
            **params,
            "with_watch_providers": provider,
            "watch_region": "JP",
        }
        results = make_request(url, provider_params).get("results", [])
        all_results.extend(results)

    # 結果の一意化
    return list({movie["id"]: movie for movie in all_results}.values())


def get_movie_details(movie_id):
    """詳細情報取得"""
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "ja-JP"}

    movie_details = make_request(base_url, params)

    images_url = f"{base_url}/images"
    images_params = {"api_key": TMDB_API_KEY}
    images_data = make_request(images_url, images_params)

    still_urls = [
        f"https://image.tmdb.org/t/p/original{img['file_path']}"
        for img in images_data.get("backdrops", [])
    ]
    still_paths_str = ",".join(still_urls)

    return {
        "title": movie_details.get("title", "不明"),
        "overview": movie_details.get("overview", "情報がありません"),
        "release_date": movie_details.get("release_date", "不明"),
        "genres": [
            genre.get("name", "不明") for genre in movie_details.get("genres", [])
        ],
        "runtime": movie_details.get("runtime", "不明"),
        "stills": still_paths_str,
    }
