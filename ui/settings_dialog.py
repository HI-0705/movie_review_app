from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton
from services.database import save_selected_subscriptions, load_selected_subscriptions
from services.movie_api import get_subscription_providers

class SubscriptionSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ｾｯﾃｨﾝｸﾞ")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout(self)
        self.subscription_checkboxes = {}

        self.initialize_checkboxes()

        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(save_button)

    def initialize_checkboxes(self):
        """ﾁｪｯｸﾎﾞｯｸｽ設定"""
        selected_ids = load_selected_subscriptions()    # ﾁｪｯｸﾎﾞｯｸｽ状態読み込み
        providers = get_subscription_providers()        # ﾌﾟﾛﾊﾞｲﾀﾞ情報取得

        # APIから提供される全てのﾌﾟﾛﾊﾞｲﾀﾞのﾁｪｯｸﾎﾞｯｸｽを作成
        for provider in providers:
            checkbox = QCheckBox(provider["name"])
            checkbox.setChecked(provider["id"] in selected_ids)
            self.layout.addWidget(checkbox)
            self.subscription_checkboxes[provider["name"]] = (provider["id"], checkbox)

    def save_settings(self):
        """設定保存"""
        selected_ids = [
            provider_id
            for _, (provider_id, checkbox) in self.subscription_checkboxes.items()
            if checkbox.isChecked() # ﾁｪｯｸされているﾌﾟﾛﾊﾞｲﾀﾞIDを取得
        ]
        # 設定を保存
        save_selected_subscriptions(selected_ids)
        self.accept()
