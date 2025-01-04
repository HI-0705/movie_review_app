import sys
import unittest
from unittest.mock import patch, Mock
from main import main

class TestMainFunction(unittest.TestCase):
    @patch("main.init_db")
    @patch("main.MainWindow")
    @patch("main.QApplication")
    @patch("sys.exit")
    def test_main(self, mock_exit, mock_qapplication, mock_mainwindow, mock_init_db):
        """main関数の動作確認"""
        # Mock
        mock_app_instance = Mock()
        mock_qapplication.return_value = mock_app_instance
        mock_window_instance = Mock()
        mock_mainwindow.return_value = mock_window_instance

        # main
        main()

        # init_db
        mock_init_db.assert_called_once()

        # QApplication初期化
        mock_qapplication.assert_called_once_with(sys.argv)

        # MainWindow
        mock_mainwindow.assert_called_once()
        mock_window_instance.show.assert_called_once()

        # 終了処理
        mock_app_instance.exec.assert_called_once()
        mock_exit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
