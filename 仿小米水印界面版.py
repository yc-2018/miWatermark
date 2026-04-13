# By：仰晨
# 文件名：仿小米水印界面版
# 时 间：2023/5/29 1:26

# By：仰晨
# 文件名：qt的demo2.0
# 时 间：2023/5/28 23:17

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon  # logo图标
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

from 批量加大水印 import add_watermark


class FileDropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        watermark_type = {'白色水印': False, '黑色水印': True}
        logos = {'小米': 'mi.png', '莱卡': 'Leica.png', '苹果': 'Apple.png', '其他': 'yc.png'}

        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                print(f'File path: {path}')
                # 水印类型（黑。or 白）
                watermark_type_value = self.parent().watermark_type.currentText()
                black = watermark_type[watermark_type_value]
                print(f'黑色水印吗 value: {black}')
                # logo
                camera_logo_value = self.parent().camera_logo.currentText()
                logo = logos[camera_logo_value]
                print(f'logo value: {logo}')
                # 相机名字
                camera_name_value = self.parent().camera_name.text()
                camera_name = camera_name_value if camera_name_value else None
                print(f'相机名字 value: {camera_name}')
                # 地点
                place_name_value = self.parent().Place_name.text()
                place = place_name_value if place_name_value else '在宇宙一颗蔚蓝的星球上'
                print(f'地点 value: {place}')

                # 是否是文件夹
                if os.path.isdir(path):
                    if not os.path.isdir(path + '加水印'):
                        os.mkdir(path + '加水印')
                    [
                        add_watermark([path, f], black=black, logo=logo, camera_name=camera_name, place=place)
                        for f in os.listdir(path)
                        if f.endswith('.jpg')
                    ]
                # 是否是单个文件
                elif os.path.isfile(path) and path.endswith('.jpg'):
                    add_watermark(
                        [os.path.dirname(path), os.path.basename(path)],
                        black=black,
                        logo=logo,
                        camera_name=camera_name,
                        place=place,
                        is_img=True,
                    )
                else:
                    print('路径有误')


class SimpleDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        :param self.watermark_type: QComboBox 一个下拉列表框，用于选择水印类型。
        """
        self.setWindowTitle('生成小米款大水印')
        self.resize(800, 400)
        # 设置窗口图标
        self.setWindowIcon(QIcon('watermark/mi.png'))

        main_layout = QVBoxLayout()  # 垂直布局，用于按从上到下的顺序排列控件，形成一列。

        # 创建第一行的下拉框和输入框
        controls_layout = QHBoxLayout()

        # 相机水印颜色--下拉框
        self.watermark_type = QComboBox(self)
        self.watermark_type.addItems(['白色水印', '黑色水印'])
        controls_layout.addWidget(self.watermark_type)

        # 相机logo--下拉框
        self.camera_logo = QComboBox(self)
        self.camera_logo.addItems(['小米', '莱卡', '苹果', '其他'])
        controls_layout.addWidget(self.camera_logo)

        # 相机名字--输入框
        self.camera_name = QLineEdit(self)
        self.camera_name.setPlaceholderText('相机名字，一般默认就行，出现不是手机名字的就自行设置')
        controls_layout.addWidget(self.camera_name)

        main_layout.addLayout(controls_layout)

        # 创建第二行的输入框
        controls_layout2 = QHBoxLayout()
        # 地点名字--输入框
        self.Place_name = QLineEdit(self)
        self.Place_name.setPlaceholderText('当在照片里面读取不到位置是就会用这个来代替，默认："在宇宙一颗蔚蓝的星球上"')
        controls_layout2.addWidget(self.Place_name)
        main_layout.addLayout(controls_layout2)

        # 创建一个接收拖动进来的文件的控件
        self.label = FileDropLabel('将文件夹或文件拖放到此处', self)
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label)

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = SimpleDemo()
    demo.show()

    sys.exit(app.exec_())
