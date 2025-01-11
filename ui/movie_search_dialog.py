from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QListWidget,
)
from PyQt6.QtCore import pyqtSignal
from services.movie_api import search_movies


class MovieSearchDialog(QDialog):
    movie_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ﾚﾋﾞｭｰ作成")
        self.setMinimumSize(400, 300)

        # 検索ﾎﾞｯｸｽﾚｲｱｳﾄ
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # 入力ﾌｨｰﾙﾄﾞ
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("映画名を入力")

        # ﾎﾞﾀﾝ作成
        self.search_button = QPushButton("検索作成")
        self.manual_create_button = QPushButton("手動作成")
        top_layout.addWidget(self.search_button)
        top_layout.addWidget(self.manual_create_button)

        # 検索結果
        self.result_list = QListWidget()

        # ｳｨｼﾞｪｯﾄ追加
        layout.addWidget(self.search_input)
        layout.addLayout(top_layout)
        layout.addWidget(self.result_list)

        self.setLayout(layout)

        # ﾎﾞﾀﾝ押下時のｲﾍﾞﾝﾄ接続
        self.search_button.clicked.connect(self.perform_search)
        self.manual_create_button.clicked.connect(self.manual_review)
        self.result_list.itemClicked.connect(self.select_movie)

    def perform_search(self):
        """ﾀｲﾄﾙ検索"""
        query = self.search_input.text()
        if not query:
            self.result_list.clear()
            self.result_list.addItem("映画名を入力してください")
            return

        # 入力された文字列で検索
        results = search_movies(query)
        self.result_list.clear()

        # 検索結果をﾘｽﾄへ追加
        if results:
            for movie in results:
                title = movie.get("title")
                release_date = movie.get("release_date", "不明")
                self.result_list.addItem(f"{title} ({release_date})")
        else:
            self.result_list.addItem("該当する項目なし")

    def select_movie(self, item):
        """検索作成ﾎﾞﾀﾝ"""
        movie_title = item.text().split(" (")[0]
        self.movie_selected.emit(movie_title)
        self.accept()

    def manual_review(self):
        """手動作成ﾎﾞﾀﾝ"""
        self.movie_selected.emit("")
        self.accept()
