import requests
from PyQt6.QtWidgets import (
    QDialog, QMessageBox, QVBoxLayout, QListWidgetItem,
    QLabel, QPushButton, QCheckBox
)
from services.movie_api import (
    get_movies_genre_list,
    search_movies_by_filters,
    get_movie_details,
    get_subscription_providers,
)
from services.database import add_to_watchlist, get_watchlist, load_selected_subscriptions
from ui.ui_movie_filter_dialog import Ui_MovieFilterDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MovieFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("検索ﾒﾆｭｰ")
        
        # UI設定
        self.ui = Ui_MovieFilterDialog()
        self.ui.setupUi(self)
        self.ui.search_button.clicked.connect(self.search_movies)
        self.ui.result_list.itemClicked.connect(self.show_movie_details)
        self.subscription_mapping = {}
        self.initialize_subscription_checkboxes()
        self.initialize_genre_combobox()

    def initialize_genre_combobox(self):
        """ｼﾞｬﾝﾙﾎﾞｯｸｽ設定"""
        genres = get_movies_genre_list()
        for genre in genres:
            self.ui.genre_combobox.addItem(genre["name"], genre["id"])

    def initialize_subscription_checkboxes(self):
        """ｻﾌﾞｽｸﾁｪｯｸﾎﾞｯｸｽ設定"""
        selected_ids = load_selected_subscriptions()
        providers = get_subscription_providers()

        for provider in providers:
            if provider["id"] in selected_ids:
                checkbox = QCheckBox(provider["name"], self.ui.subscription_groupbox)
                checkbox.setChecked(provider["id"] in selected_ids)
                self.ui.subscription_groupbox.layout().addWidget(checkbox)
                self.subscription_mapping[provider["name"]] = (provider["id"], checkbox)

    def search_movies(self):
        """ﾌｨﾙﾀ検索処理"""
        genre_id = self.ui.genre_combobox.currentData() # ｼﾞｬﾝﾙ
        year = self.ui.year_combobox.currentText()      # 公開年
        subscriptions = [                               # ｻﾌﾞｽｸﾁｪｯｸﾎﾞｯｸｽ
            provider_id
            for _, (provider_id, checkbox) in self.subscription_mapping.items()
            if checkbox.isChecked()
        ]

        try:
            results = search_movies_by_filters(
                genre=None if genre_id == -1 else genre_id,
                year=None if year == 0 else year,
                subscriptions=subscriptions
            )
            self.display_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"検索に失敗しました: {str(e)}")

    def display_results(self, movies):
        """検索結果表示"""
        self.ui.result_list.clear()
        if not movies:
            self.ui.result_list.addItem("該当項目なし")
            return

        # 該当するﾀｲﾄﾙをﾘｽﾄに追加
        for movie in movies:
            title = movie.get("title", "ﾀｲﾄﾙ不明")
            movie_id = movie.get("id", None)
            item = QListWidgetItem(title)
            item.setData(1, movie_id)
            self.ui.result_list.addItem(item)

    def show_movie_details(self, item):
        """詳細ﾀﾞｲｱﾛｸﾞ表示"""
        movie_id = item.data(1)
        title = item.text()

        if not movie_id:
            QMessageBox.critical(self, "Error", "詳細の取得に失敗しました")
            return

        # あらすじとｽﾁﾙ画像を入れた詳細ﾀﾞｲｱﾛｸﾞを表示
        try:
            details = get_movie_details(movie_id)
            overview = (details.get("overview", "").strip() or "映画のあらすじが見つかりませんでした")
            still_paths = details.get("stills", "").split(",")
            self.create_details_dialog(movie_id, title, overview, still_paths)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"詳細の取得に失敗しました: {str(e)}")

    def create_details_dialog(self, movie_id, title, overview, still_paths):
        """詳細ﾀﾞｲｱﾛｸﾞ作成"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"あらすじ - {title}")
        dialog.setMinimumSize(300, 150)

        layout = QVBoxLayout(dialog)

        # ｽﾁﾙ画像生成
        if still_paths and still_paths[0]:
            still_url = f"https://image.tmdb.org/t/p/w500{still_paths[0]}"
            image_data = requests.get(still_url).content

            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            label_image = QLabel()
            label_image.setPixmap(pixmap)
            label_image.setScaledContents(True)
            label_image.setFixedSize(350, 220)
            layout.addWidget(label_image)
            layout.setAlignment(label_image, Qt.AlignmentFlag.AlignCenter)

        # あらすじ生成
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        
        # ｳｫｯﾁﾘｽﾄﾎﾞﾀﾝ生成
        watchlist_button = QPushButton("ｳｫｯﾁﾘｽﾄに追加")

        # ﾚｲｱｳﾄに追加
        layout.addWidget(overview_label)
        layout.addWidget(watchlist_button)
        dialog.setLayout(layout)

        # 登録済みのﾀｲﾄﾙはｳｫｯﾁﾘｽﾄﾎﾞﾀﾝを無効化
        watchlist_titles = [item[1] for item in get_watchlist()]
        if title in watchlist_titles:
            watchlist_button.setText("ｳｫｯﾁﾘｽﾄに追加済み")
            watchlist_button.setEnabled(False)
        else:
            watchlist_button.clicked.connect(lambda: self.add_to_watchlist(movie_id, title, watchlist_button))

        dialog.exec()

    def add_to_watchlist(self, movie_id, title, button):
        """ｳｫｯﾁﾘｽﾄ追加"""
        add_to_watchlist(movie_id, title)
        button.setText("ｳｫｯﾁﾘｽﾄに追加しました")
        button.setEnabled(False)
