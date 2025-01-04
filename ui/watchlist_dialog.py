import requests
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox
    )
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from services.database import get_watchlist, remove_from_watchlist
from services.movie_api import get_movie_details

class WatchlistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ｳｫｯﾁﾘｽﾄ")
        self.setMinimumSize(400, 400)

        # ﾚｲｱｳﾄ設定
        layout = QVBoxLayout(self)

        # ﾃｰﾌﾞﾙｳｨｼﾞｪｯﾄ設定
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ﾀｲﾄﾙ", "あらすじ", "削除"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # 列幅調整
        self.table.setColumnWidth(0, 210)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 75)
        
        layout.addWidget(self.table)

        # ｳｫｯﾁﾘｽﾄ表示
        self.load_watchlist()

    def load_watchlist(self):
        """ｳｫｯﾁﾘｽﾄ表示"""
        self.table.setRowCount(0)
        watchlist = get_watchlist()

        if not watchlist:
            QMessageBox.information(self, "Info", "ｳｫｯﾁﾘｽﾄが空です。")
            return

        watchlist = sorted(watchlist, key=lambda x: x[1])  # ﾀｲﾄﾙ昇順ｿｰﾄ

        # ﾀｲﾄﾙ毎に表示
        for row_index, (movie_id, title, _) in enumerate(watchlist):
            self.table.insertRow(row_index)

            # ﾀｲﾄﾙ
            title_item = QTableWidgetItem(title)
            self.table.setItem(row_index, 0, title_item)

            # 詳細表示処理
            detail_button = QPushButton("info", self)
            detail_button.clicked.connect(lambda _, mid=movie_id, t=title: self.show_movie_details(mid, t))
            self.table.setCellWidget(row_index, 1, detail_button)

            # 削除処理
            delete_button = QPushButton("del", self)
            delete_button.clicked.connect(lambda _, mid=movie_id: self.delete_from_watchlist(mid))
            self.table.setCellWidget(row_index, 2, delete_button)

    def show_movie_details(self, movie_id, title):
        """詳細表示処理"""
        if not movie_id:
            QMessageBox.critical(self, "Error", "詳細の取得に失敗しました")
            return

        # 詳細情報取得
        try:
            details = get_movie_details(movie_id)
            overview = (details.get("overview", "").strip() or "映画の詳細が見つかりませんでした")
            still_paths = details.get("stills", "").split(",")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"詳細を取得できませんでした: {str(e)}")
            return

        # 詳細情報ﾀﾞｲｱﾛｸﾞ作成
        dialog = QDialog(self)
        dialog.setWindowTitle(f"あらすじ - {title}")
        dialog.setMinimumSize(300, 200)

        layout = QVBoxLayout(dialog)

        # ｽﾁﾙ画像表示処理
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

        # あらすじ表示
        overview_label = QLabel(overview)
        overview_label.setWordWrap(True)
        layout.addWidget(overview_label)

        dialog.exec()
        self.load_watchlist()   # 再読み込み

    def delete_from_watchlist(self, movie_id):
        """ｳｫｯﾁﾘｽﾄ削除"""
        try:
            remove_from_watchlist(movie_id)
            QMessageBox.information(self, "Success", "削除しました。")
            self.load_watchlist()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"削除に失敗しました: {str(e)}")
