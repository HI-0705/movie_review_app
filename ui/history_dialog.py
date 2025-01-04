from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidgetItem,
    QTableWidget, QPushButton
    )
from PyQt6.QtCore import Qt
from ui.review_dialog import ReviewDialog
from services.database import get_reviews

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ﾚﾋﾞｭｰ履歴")
        self.setMinimumSize(500, 300)
        
        layout = QVBoxLayout()

        # ﾃｰﾌﾞﾙｳｨｼﾞｪｯﾄ設定
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["ﾀｲﾄﾙ", "記載日", "ｽｺｱ", "ﾁｪｯｸ"])
        
        # 列幅調整
        self.table_widget.setColumnWidth(0, 245)
        self.table_widget.setColumnWidth(1, 130)
        self.table_widget.setColumnWidth(2, 35)
        self.table_widget.setColumnWidth(3, 50)
        
        layout.addWidget(self.table_widget)

        # 閉じるﾎﾞﾀﾝ設定
        close_button = QPushButton("閉じる")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        
        # 既存のﾚﾋﾞｭｰを読み込む
        self.load_reviews()

    def load_reviews(self):
        """ﾚﾋﾞｭｰ履歴読み込み"""
        self.table_widget.setRowCount(0)
        reviews = get_reviews()
        reviews.sort(key=lambda review: review[1])  # ﾀｲﾄﾙ昇順ｿｰﾄ
        for review in reviews:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            # ﾚﾋﾞｭｰ履歴の基本情報
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(review[1]))         # ﾀｲﾄﾙ
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(review[4]))         # 記載日
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(review[3])))    # 評価

            # ﾚﾋﾞｭｰ内容確認ﾎﾞﾀﾝ
            edit_button = QPushButton("内容")
            edit_button.clicked.connect(lambda _, r=review: self.open_review_detail(r))
            self.table_widget.setCellWidget(row_position, 3, edit_button)

    def open_review_detail(self, review_data):
        """ﾚﾋﾞｭｰﾀﾞｲｱﾛｸﾞを編集ﾓｰﾄﾞで開く"""
        dialog = ReviewDialog(self, review_data)
        dialog.review_updated.connect(self.load_reviews)
        dialog.exec()
        self.load_reviews() # 再読み込み