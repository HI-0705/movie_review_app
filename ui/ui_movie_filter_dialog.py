from PyQt6 import QtWidgets
from datetime import datetime
from services.movie_api import get_movies_genre_list


class Ui_MovieFilterDialog:
    def setupUi(self, MovieFilterDialog: QtWidgets.QDialog):
        MovieFilterDialog.setObjectName("MovieFilterDialog")
        MovieFilterDialog.resize(400, 500)
        self.create_layout(MovieFilterDialog)
        self.add_genre_combobox()
        self.add_year_combobox()
        self.add_subscription_groupbox()
        self.add_search_button()
        self.add_result_list()

    def create_layout(self, parent: QtWidgets.QWidget):
        # ﾚｲｱｳﾄ作成
        self.verticalLayout = QtWidgets.QVBoxLayout(parent)
        self.verticalLayout.setObjectName("verticalLayout")

    def add_genre_combobox(self):
        # ｼﾞｬﾝﾙﾎﾞｯｸｽ
        self.genre_combobox = self.create_combobox("genre_combobox", "All-Genres", -1)
        genres = get_movies_genre_list()
        for genre in genres:
            self.genre_combobox.addItem(genre["name"], genre["id"])
        self.verticalLayout.addWidget(self.genre_combobox)

    def add_year_combobox(self):
        # 公開年ﾎﾞｯｸｽ
        self.year_combobox = self.create_combobox(
            "year_combobox", "All-ReleaseYears", -1
        )
        current_year = datetime.now().year
        for year in range(current_year, 1949, -1):
            self.year_combobox.addItem(str(year))
        self.verticalLayout.addWidget(self.year_combobox)

    def add_subscription_groupbox(self):
        # ｻﾌﾞｽｸﾎﾞｯｸｽ
        self.subscription_groupbox = QtWidgets.QGroupBox("Subscription")
        self.subscription_groupbox.setObjectName("subscription_groupbox")
        self.subscription_layout = QtWidgets.QVBoxLayout(self.subscription_groupbox)
        self.subscription_layout.setObjectName("subscription_layout")
        self.verticalLayout.addWidget(self.subscription_groupbox)

    def add_search_button(self):
        # 検索ﾎﾞﾀﾝ
        self.search_button = QtWidgets.QPushButton("検索")
        self.search_button.setObjectName("search_button")
        self.verticalLayout.addWidget(self.search_button)

    def add_result_list(self):
        # 検索結果ﾘｽﾄ
        self.result_list = QtWidgets.QListWidget()
        self.result_list.setObjectName("result_list")
        self.verticalLayout.addWidget(self.result_list)

    @staticmethod
    def create_combobox(
        name: str, default_text: str, default_data: int
    ) -> QtWidgets.QComboBox:
        """ｺﾝﾎﾞﾎﾞｯｸｽ作成"""
        combobox = QtWidgets.QComboBox()
        combobox.setObjectName(name)
        combobox.addItem(default_text, default_data)
        return combobox
