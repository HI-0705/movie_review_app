from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QPushButton,
    QMessageBox,
)
from services.database import execute_query


class ReviewDialog(QDialog):
    review_updated = pyqtSignal()

    def __init__(self, parent=None, review_data=None):
        super().__init__(parent)
        self.setWindowTitle("ｴﾃﾞｨｯﾄ" if review_data else "ｸﾘｴｲﾄ")
        self.review_data = review_data
        self.setup_ui()
        if self.review_data:
            self.load_review_data()

    def setup_ui(self):
        """UI初期化"""
        layout = QVBoxLayout()

        # ﾀｲﾄﾙ
        layout.addWidget(QLabel("ﾀｲﾄﾙ"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        # 感想
        layout.addWidget(QLabel("ﾚﾋﾞｭｰ"))
        self.review_input = QTextEdit()
        layout.addWidget(self.review_input)

        # 評価
        layout.addWidget(QLabel("ｽｺｱ (1-5)"))
        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        layout.addWidget(self.rating_input)

        # 保存
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_review)
        layout.addWidget(self.save_button)

        # 編集ﾓｰﾄﾞでは削除ﾎﾞﾀﾝを表示
        if self.review_data:
            self.delete_button = QPushButton("削除")
            self.delete_button.clicked.connect(self.delete_review)
            layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def load_review_data(self):
        """既存ﾃﾞｰﾀﾛｰﾄﾞ"""
        self.title_input.setText(self.review_data[1])
        self.review_input.setText(self.review_data[2])
        self.rating_input.setValue(self.review_data[3])
        self.title_input.setReadOnly(True)

    def save_review(self):
        """ﾚﾋﾞｭｰ保存"""
        title = self.title_input.text().strip()
        review = self.review_input.toPlainText().strip()
        rating = self.rating_input.value()

        # 入力ﾁｪｯｸ
        if not title or not review:
            QMessageBox.warning(self, "Error", "入力されていない項目があります")
            return

        # ﾓｰﾄﾞ別でｸｴﾘを設定
        if self.review_data:  # 編集
            query = """
            UPDATE reviews SET review = ?, rating = ?, created_at = datetime('now', 'localtime')
            WHERE id = ?
            """
            params = (review, rating, self.review_data[0])
        else:  # 新規
            query = """
            INSERT INTO reviews (title, review, rating, created_at)
            VALUES (?, ?, ?, datetime('now', '+9 hours'))
            """
            params = (title, review, rating)

        # ﾃﾞｰﾀﾍﾞｰｽ更新
        try:
            execute_query(query, params)
            QMessageBox.information(self, "Success", "保存しました")
            self.review_updated.emit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failure: {e}")

    def delete_review(self):
        """ﾚﾋﾞｭｰ削除"""
        confirm = QMessageBox.question(
            self,
            "Confirm",
            "削除しますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                query = "DELETE FROM reviews WHERE id = ?"
                execute_query(query, (self.review_data[0],))
                QMessageBox.information(self, "Success", "削除しました")
                self.review_updated.emit()
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failure: {e}")
