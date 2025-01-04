from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from ui.review_dialog import ReviewDialog
from ui.settings_dialog import SubscriptionSettingsDialog
from ui.movie_search_dialog import MovieSearchDialog
from ui.movie_filter_dialog import MovieFilterDialog
from ui.history_dialog import HistoryDialog
from ui.watchlist_dialog import WatchlistDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MovieReviewApp")   # ｳｨﾝﾄﾞｳﾀｲﾄﾙ設定
        self.setMinimumSize(300, 100)           # 最小ｻｲｽﾞ設定
        self.setup_ui()

    def setup_ui(self):
        """UI初期化"""
        layout = QVBoxLayout()
        buttons = {
            "Review": self.open_movie_search_for_review,
            "History": self.open_history_dialog,
            "Search": self.open_movie_filter_dialog,
            "Watchlist": self.open_watchlist_dialog,
            "Setting": self.open_settings_dialog
        }
        # ﾎﾞﾀﾝを作成してﾚｲｱｳﾄに追加
        for name, method in buttons.items():
            button = QPushButton(name)
            button.clicked.connect(method)
            layout.addWidget(button)

        # ｳｨｼﾞｪｯﾄを設定
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def safe_exec_dialog(self, dialog_class):
        """ﾀﾞｲｱﾛｸﾞ生成"""
        try:
            dialog = dialog_class()
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"dialog open error: {e}")

    def open_movie_search_for_review(self):
        """ﾀｲﾄﾙ検索"""
        dialog = MovieSearchDialog()
        dialog.movie_selected.connect(self.show_review_dialog)
        dialog.exec()

    def show_review_dialog(self, movie_title):
        """ﾚﾋﾞｭｰ作成"""
        dialog = ReviewDialog()
        dialog.title_input.setText(movie_title)
        dialog.exec()

    def open_history_dialog(self):
        """ﾚﾋﾞｭｰ履歴"""
        self.safe_exec_dialog(HistoryDialog)

    def open_movie_filter_dialog(self):
        """ﾌｨﾙﾀ検索"""
        self.safe_exec_dialog(MovieFilterDialog)

    def open_watchlist_dialog(self):
        """ｳｫｯﾁﾘｽﾄ"""
        self.safe_exec_dialog(WatchlistDialog)

    def open_settings_dialog(self):
        """ｻﾌﾞｽｸ設定"""
        self.safe_exec_dialog(SubscriptionSettingsDialog)