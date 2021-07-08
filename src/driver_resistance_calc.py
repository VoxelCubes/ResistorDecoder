import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
from PySide6.QtSvgWidgets import QSvgWidget
import PySide6.QtWidgets as Qw

import helpers as gh
import smd_code_parser as smd_parse
from ui_generated_files.ui_resistance_calc import Ui_MainWindow
from driver_license import LicenseAgreement



class ResistanceCalc(Qw.QMainWindow, Ui_MainWindow):
    """Wrapper to handle interactions on the Unit Manager level."""


    def __init__(self):
        Qw.QMainWindow.__init__(self)
        self.setupUi(self)

        icon = Qg.QIcon()
        icon.addFile(":/general/resistor_icon.svg", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Resistor Decoder")


        # For the license window
        self.license_window = None

        self.populate_combo_boxes()

        # Set the default tolerance to the most common band, gold
        self.comboBox_t_4b.setCurrentIndex(2)
        self.comboBox_t_5b.setCurrentIndex(1)
        self.comboBox_t_6b.setCurrentIndex(1)
        # Set the default multiplier to 1
        self.comboBox_m_4b.setCurrentIndex(3)
        self.comboBox_m_5b.setCurrentIndex(3)
        self.comboBox_m_6b.setCurrentIndex(3)

        # Initialize SVG widgets
        self.svg_widget_4b = QSvgWidget(self.tab_4b)
        self.horizontalLayout_4b_svg.insertWidget(1, self.svg_widget_4b)
        self.svg_widget_4b.renderer().setAspectRatioMode(Qc.Qt.KeepAspectRatio)
        self.svg_widget_4b.setFixedSize(Qc.QSize(445, 100))

        self.svg_widget_5b = QSvgWidget(self.tab_5b)
        self.horizontalLayout_5b_svg.insertWidget(1, self.svg_widget_5b)
        self.svg_widget_5b.renderer().setAspectRatioMode(Qc.Qt.KeepAspectRatio)
        self.svg_widget_5b.setFixedSize(Qc.QSize(445, 100))

        self.svg_widget_6b = QSvgWidget(self.tab_6b)
        self.horizontalLayout_6b_svg.insertWidget(1, self.svg_widget_6b)
        self.svg_widget_6b.renderer().setAspectRatioMode(Qc.Qt.KeepAspectRatio)
        self.svg_widget_6b.setFixedSize(Qc.QSize(445, 100))

        self.svg_widget_smd = QSvgWidget(self.tab_smd)
        self.horizontalLayout_smd_svg.insertWidget(1, self.svg_widget_smd)
        self.svg_widget_smd.renderer().setAspectRatioMode(Qc.Qt.KeepAspectRatio)
        self.svg_widget_smd.setFixedSize(Qc.QSize(300, 126))
        # Add the lineEdit over the smd preview
        self.smd_line_edit = Qw.QLineEdit(self.svg_widget_smd)
        self.smd_line_edit.setFixedSize(Qc.QSize(300, 126))
        self.smd_line_edit.setFrame(False)
        self.smd_line_edit.setAlignment(Qg.Qt.AlignHCenter)
        # Set a simple default smd code
        self.smd_line_edit.setText("102")
        # Set magic font size appropriate for the hard-coded size
        smd_font = Qg.QFont()
        smd_font.setPointSize(44)
        self.smd_line_edit.setFont(smd_font)
        self.smd_line_edit.setMaxLength(4)
        self.smd_line_edit.setStyleSheet("background: transparent; color: white")
        # Hide the warning and notice for smd values
        self.label_code_invalid_icon.hide()
        self.label_code_invalid_label.hide()
        self.label_tolerance_notice.hide()

        # Connect license button slot
        self.pushButton_license.clicked.connect(self.open_license)
        # Connect slots to update the output
        self.comboBox_1d_4b.currentIndexChanged.connect(self.calculate_res_4b)
        self.comboBox_2d_4b.currentIndexChanged.connect(self.calculate_res_4b)
        self.comboBox_m_4b.currentIndexChanged.connect(self.calculate_res_4b)
        self.comboBox_t_4b.currentIndexChanged.connect(self.calculate_res_4b)

        self.comboBox_1d_5b.currentIndexChanged.connect(self.calculate_res_5b)
        self.comboBox_2d_5b.currentIndexChanged.connect(self.calculate_res_5b)
        self.comboBox_3d_5b.currentIndexChanged.connect(self.calculate_res_5b)
        self.comboBox_m_5b.currentIndexChanged.connect(self.calculate_res_5b)
        self.comboBox_t_5b.currentIndexChanged.connect(self.calculate_res_5b)

        self.comboBox_1d_6b.currentIndexChanged.connect(self.calculate_res_6b)
        self.comboBox_2d_6b.currentIndexChanged.connect(self.calculate_res_6b)
        self.comboBox_3d_6b.currentIndexChanged.connect(self.calculate_res_6b)
        self.comboBox_m_6b.currentIndexChanged.connect(self.calculate_res_6b)
        self.comboBox_t_6b.currentIndexChanged.connect(self.calculate_res_6b)
        self.comboBox_tcr_6b.currentIndexChanged.connect(self.calculate_res_6b)

        self.radioButton_line_none.clicked.connect(self.calculate_res_smd)
        self.radioButton_line_top.clicked.connect(self.calculate_res_smd)
        self.radioButton_line_under_short.clicked.connect(self.calculate_res_smd)
        self.radioButton_line_under_long.clicked.connect(self.calculate_res_smd)
        self.smd_line_edit.textEdited.connect(self.calculate_res_smd)

        self.color_lookup = [b"#000000",  # Colors as specified by the IEC.
                             b"#800000",
                             b"#FF0000",
                             b"#FF9900",
                             b"#FFFF00",
                             b"#00B050",
                             b"#0070C0",
                             b"#9900FF",
                             b"#A6A6A6",
                             b"#FFFFFF",
                             b"#FFD100",
                             b"#DDDDDD",
                             b"#FFDDFF"
                             ]

        with open("../icons/resistor_4b.svg", "rb") as svg_file:
            self.svg_data_4b = svg_file.read()
        with open("../icons/resistor_5b.svg", "rb") as svg_file:
            self.svg_data_5b = svg_file.read()
        with open("../icons/resistor_6b.svg", "rb") as svg_file:
            self.svg_data_6b = svg_file.read()
        with open("../icons/resistor_smd.svg", "rb") as svg_file:
            self.svg_data_smd = svg_file.read()

        self.change_band_colors_4b()

        # Fill initial state in outputs
        self.calculate_res_4b()
        self.calculate_res_5b()
        self.calculate_res_6b()
        self.calculate_res_smd()


    def change_band_colors_4b(self):
        idx1 = self.comboBox_1d_4b.currentIndex() + 1  # Black not available, skipping 0 index
        idx2 = self.comboBox_2d_4b.currentIndex()
        idm = self.comboBox_m_4b.currentIndex()
        idt = self.comboBox_t_4b.currentIndex() + 1  # Black not available, skipping 0 index
        # Shift values down by 3 unless reaching the end. The last 3 colors were moved to the front.
        idt -= 3
        if idt <= 0:
            idt = 10 - idt
        # Correct coloring order for the multiplier band
        idm -= 3
        if idm < 0:
            idm = 9 - idm
        # Hot patch SVG file
        current_data = self.svg_data_4b.replace(b"#400001", self.color_lookup[idx1]) \
                                       .replace(b"#400002", self.color_lookup[idx2]) \
                                       .replace(b"#400003", self.color_lookup[idm])

        if idt == 12:  # Make 4th band invisible if blank selected, otherwise apply color transform.
            current_data = current_data.replace(b"opacity:1;mix-blend-mode:normal;vector-effect:none;fill:#400004;",
                                                b"opacity:0;mix-blend-mode:normal;vector-effect:none;fill:#400004;")
        else:
            current_data = current_data.replace(b"#400004", self.color_lookup[idt])
        # Update SVG
        self.svg_widget_4b.load(Qc.QByteArray(current_data))
        # change_band_colors_4b


    def change_band_colors_5b(self):
        idx1 = self.comboBox_1d_5b.currentIndex() + 1  # Black not available, skipping 0 index
        idx2 = self.comboBox_2d_5b.currentIndex()
        idx3 = self.comboBox_3d_5b.currentIndex()
        idm = self.comboBox_m_5b.currentIndex()
        idt = self.comboBox_t_5b.currentIndex() + 1  # Black not available, skipping 0 index
        # Shift values down by 3 unless reaching the end. The last 3 colors were moved to the front.
        idt -= 2
        if idt <= 0:
            idt = 10 - idt
        # Correct coloring order for the multiplier band
        idm -= 3
        if idm < 0:
            idm = 9 - idm
        # Hot patch SVG file
        current_data = self.svg_data_5b.replace(b"#500001", self.color_lookup[idx1]) \
                                       .replace(b"#500002", self.color_lookup[idx2]) \
                                       .replace(b"#500003", self.color_lookup[idx3]) \
                                       .replace(b"#500004", self.color_lookup[idm]) \
                                       .replace(b"#500005", self.color_lookup[idt])
        # Update SVG
        self.svg_widget_5b.load(Qc.QByteArray(current_data))
        # change_band_colors_5b


    def change_band_colors_6b(self):
        idx1 = self.comboBox_1d_6b.currentIndex() + 1  # Black not available, skipping 0 index
        idx2 = self.comboBox_2d_6b.currentIndex()
        idx3 = self.comboBox_3d_6b.currentIndex()
        idm = self.comboBox_m_6b.currentIndex()
        idt = self.comboBox_t_6b.currentIndex() + 1  # Black not available, skipping 0 index
        idc = self.comboBox_tcr_6b.currentIndex()
        # Shift values down by 3 unless reaching the end. The last 3 colors were moved to the front.
        idt -= 2
        if idt <= 0:
            idt = 10 - idt
        # Correct coloring order for the multiplier band
        idm -= 3
        if idm < 0:
            idm = 9 - idm
        # Hot patch SVG file
        current_data = self.svg_data_6b.replace(b"#600001", self.color_lookup[idx1]) \
            .replace(b"#600002", self.color_lookup[idx2]) \
            .replace(b"#600003", self.color_lookup[idx3]) \
            .replace(b"#600004", self.color_lookup[idm]) \
            .replace(b"#600005", self.color_lookup[idt]) \
            .replace(b"#600006", self.color_lookup[idc])
        # Update SVG
        self.svg_widget_6b.load(Qc.QByteArray(current_data))
        # change_band_colors_6b


    def change_band_colors_smd(self):
        line_under_short = self.radioButton_line_under_short.isChecked()
        line_under_long = self.radioButton_line_under_long.isChecked()
        line_top = self.radioButton_line_top.isChecked()


        def color_assignment(show):
            if show:
                return b"#FFFFFF"
            else:
                return b"#000000"


        def opacity_assignment(show):
            # Used to make the long bar transparent or opaque, since it overlaps the short bar.
            if show:
                return b"stroke-opacity:1"
            else:
                return b"stroke-opacity:0"


        # Hot patch SVG file by replacing these placeholder colors.
        current_data = self.svg_data_smd.replace(b"#996601", color_assignment(line_under_short)) \
            .replace(b"#996602", color_assignment(line_under_long)) \
            .replace(b"#996603", color_assignment(line_top)) \
            .replace(b"stroke-opacity:0.28", opacity_assignment(line_under_long))
        # Update SVG
        self.svg_widget_smd.load(Qc.QByteArray(current_data))
        # change_band_colors_smd


    def calculate_res_4b(self):
        self.change_band_colors_4b()  # Update svg
        digit1 = self.comboBox_1d_4b.currentText()
        digit2 = self.comboBox_2d_4b.currentText()
        multiplier = self.comboBox_m_4b.currentIndex() - 3  # scale starts at milli ohm
        tolerance = self.comboBox_t_4b.currentText()
        mantissa = int(digit1 + digit2)

        value, min_value, max_value = gh.calculate_values(tolerance, mantissa, multiplier)

        self.lineEdit_resistance_4b.setText(f"{gh.format_resistance(value, 3)} ±{tolerance}")
        self.lineEdit_resistance_min_4b.setText(gh.format_resistance(min_value, 5))
        self.lineEdit_resistance_max_4b.setText(gh.format_resistance(max_value, 5))

        return value, min_value, max_value
        # calculate_res_4b


    def calculate_res_5b(self):
        self.change_band_colors_5b()  # Update svg
        digit1 = self.comboBox_1d_5b.currentText()
        digit2 = self.comboBox_2d_5b.currentText()
        digit3 = self.comboBox_3d_5b.currentText()
        multiplier = self.comboBox_m_5b.currentIndex() - 3  # scale starts at milli ohm
        tolerance = self.comboBox_t_5b.currentText()
        mantissa = int(digit1 + digit2 + digit3)

        value, min_value, max_value = gh.calculate_values(tolerance, mantissa, multiplier)

        self.lineEdit_resistance_5b.setText(f"{gh.format_resistance(value, 3)} ±{tolerance}")
        self.lineEdit_resistance_min_5b.setText(gh.format_resistance(min_value, 5))
        self.lineEdit_resistance_max_5b.setText(gh.format_resistance(max_value, 5))

        return value, min_value, max_value
        # calculate_res_5b


    def calculate_res_6b(self):
        self.change_band_colors_6b()  # Update svg
        digit1 = self.comboBox_1d_6b.currentText()
        digit2 = self.comboBox_2d_6b.currentText()
        digit3 = self.comboBox_3d_6b.currentText()
        multiplier = self.comboBox_m_6b.currentIndex() - 3  # scale starts at milli ohm
        tolerance = self.comboBox_t_6b.currentText()
        tcr = self.comboBox_tcr_6b.currentText()
        mantissa = int(digit1 + digit2 + digit3)

        value, min_value, max_value = gh.calculate_values(tolerance, mantissa, multiplier)

        self.lineEdit_resistance_6b.setText(f"{gh.format_resistance(value, 3)} ±{tolerance}")
        self.lineEdit_resistance_min_6b.setText(gh.format_resistance(min_value, 5))
        self.lineEdit_resistance_max_6b.setText(gh.format_resistance(max_value, 5))
        self.lineEdit_tcr_6b.setText(tcr + " ppm/°C")

        return value, min_value, max_value, int(tcr[1:])
        # calculate_res_6b


    def calculate_res_smd(self):
        self.change_band_colors_smd()  # Update svg
        smd_code = self.smd_line_edit.text()
        line_under_short = self.radioButton_line_under_short.isChecked()
        line_under_long = self.radioButton_line_under_long.isChecked()
        # Top Line is irrelevant for the calculation and cosmetic only.
        # line_top = self.radioButton_line_top.isChecked()

        decoded = smd_parse.parse_code(smd_code, line_under_short, line_under_long)

        if decoded is not None:
            value, tolerance, is_standard_tolerance = decoded

            min_value = value * (1 - 0.01 * tolerance)
            max_value = value * (1 + 0.01 * tolerance)

            self.lineEdit_resistance_smd.setText(f"{gh.format_resistance(value, 3)} ±{tolerance}%")
            self.lineEdit_resistance_min_smd.setText(gh.format_resistance(min_value, 5))
            self.lineEdit_resistance_max_smd.setText(gh.format_resistance(max_value, 5))

            # Hide notice if standardized
            self.label_tolerance_notice.setHidden(is_standard_tolerance)
            # Hide warnings
            self.label_code_invalid_icon.hide()
            self.label_code_invalid_label.hide()

            return value, min_value, max_value
        else:
            # Invalid code
            self.lineEdit_resistance_smd.clear()
            self.lineEdit_resistance_min_smd.clear()
            self.lineEdit_resistance_max_smd.clear()
            # Hide notice
            self.label_tolerance_notice.hide()
            # Show warnings
            self.label_code_invalid_icon.show()
            self.label_code_invalid_label.show()

            return None, None, None
        # calculate_res_smd


    def populate_combo_boxes(self):
        icons = dict()
        icons["black"] = Qg.QIcon()
        icons["black"].addFile(":/colors/Color Squares/black.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["brown"] = Qg.QIcon()
        icons["brown"].addFile(":/colors/Color Squares/brown.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["red"] = Qg.QIcon()
        icons["red"].addFile(":/colors/Color Squares/red.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["orange"] = Qg.QIcon()
        icons["orange"].addFile(":/colors/Color Squares/orange.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["yellow"] = Qg.QIcon()
        icons["yellow"].addFile(":/colors/Color Squares/yellow.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["green"] = Qg.QIcon()
        icons["green"].addFile(":/colors/Color Squares/green.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["blue"] = Qg.QIcon()
        icons["blue"].addFile(":/colors/Color Squares/blue.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["violet"] = Qg.QIcon()
        icons["violet"].addFile(":/colors/Color Squares/violet.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["gray"] = Qg.QIcon()
        icons["gray"].addFile(":/colors/Color Squares/gray.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["white"] = Qg.QIcon()
        icons["white"].addFile(":/colors/Color Squares/white.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["gold"] = Qg.QIcon()
        icons["gold"].addFile(":/colors/Color Squares/gold.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["silver"] = Qg.QIcon()
        icons["silver"].addFile(":/colors/Color Squares/silver.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["pink"] = Qg.QIcon()
        icons["pink"].addFile(":/colors/Color Squares/pink.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)
        icons["blank"] = Qg.QIcon()
        icons["blank"].addFile(":/colors/Color Squares/blank.png", Qc.QSize(), Qg.QIcon.Normal, Qg.QIcon.Off)


        def attach_digit1(combobox):
            combobox.addItem(icons["brown"], "1")
            combobox.addItem(icons["red"], "2")
            combobox.addItem(icons["orange"], "3")
            combobox.addItem(icons["yellow"], "4")
            combobox.addItem(icons["green"], "5")
            combobox.addItem(icons["blue"], "6")
            combobox.addItem(icons["violet"], "7")
            combobox.addItem(icons["gray"], "8")
            combobox.addItem(icons["white"], "9")


        def attach_digit2(combobox):
            combobox.addItem(icons["black"], "0")
            combobox.addItem(icons["brown"], "1")
            combobox.addItem(icons["red"], "2")
            combobox.addItem(icons["orange"], "3")
            combobox.addItem(icons["yellow"], "4")
            combobox.addItem(icons["green"], "5")
            combobox.addItem(icons["blue"], "6")
            combobox.addItem(icons["violet"], "7")
            combobox.addItem(icons["gray"], "8")
            combobox.addItem(icons["white"], "9")


        def attach_digit3(combobox):
            combobox.addItem(icons["black"], "0")
            combobox.addItem(icons["brown"], "1")
            combobox.addItem(icons["red"], "2")
            combobox.addItem(icons["orange"], "3")
            combobox.addItem(icons["yellow"], "4")
            combobox.addItem(icons["green"], "5")
            combobox.addItem(icons["blue"], "6")
            combobox.addItem(icons["violet"], "7")
            combobox.addItem(icons["gray"], "8")
            combobox.addItem(icons["white"], "9")


        def attach_multiplier(combobox):
            combobox.addItem(icons["pink"], "1 mΩ")
            combobox.addItem(icons["silver"], "10 mΩ")
            combobox.addItem(icons["gold"], "100 mΩ")
            combobox.addItem(icons["black"], "1 Ω")
            combobox.addItem(icons["brown"], "10 Ω")
            combobox.addItem(icons["red"], "100 Ω")
            combobox.addItem(icons["orange"], "1 kΩ")
            combobox.addItem(icons["yellow"], "10 kΩ")
            combobox.addItem(icons["green"], "100 kΩ")
            combobox.addItem(icons["blue"], "1 MΩ")
            combobox.addItem(icons["violet"], "10 MΩ")
            combobox.addItem(icons["gray"], "100 MΩ")
            combobox.addItem(icons["white"], "1 GΩ")


        def attach_tolerance(combobox, allow_blank=False):
            if allow_blank:
                combobox.addItem(icons["blank"], "20%")
            combobox.addItem(icons["silver"], "10%")
            combobox.addItem(icons["gold"], "5%")
            combobox.addItem(icons["brown"], "1%")
            combobox.addItem(icons["red"], "2%")
            combobox.addItem(icons["orange"], "0.05%")
            combobox.addItem(icons["yellow"], "0.02%")
            combobox.addItem(icons["green"], "0.5%")
            combobox.addItem(icons["blue"], "0.25%")
            combobox.addItem(icons["violet"], "0.1%")
            combobox.addItem(icons["gray"], "0.01%")


        def attach_tcr(combobox):
            combobox.addItem(icons["black"], "±250")
            combobox.addItem(icons["brown"], "±100")
            combobox.addItem(icons["red"], "±50")
            combobox.addItem(icons["orange"], "±15")
            combobox.addItem(icons["yellow"], "±25")
            combobox.addItem(icons["green"], "±20")
            combobox.addItem(icons["blue"], "±10")
            combobox.addItem(icons["violet"], "±5")
            combobox.addItem(icons["gray"], "±1")


        # Assign 4 Band
        attach_digit1(self.comboBox_1d_4b)
        attach_digit2(self.comboBox_2d_4b)
        attach_multiplier(self.comboBox_m_4b)
        attach_tolerance(self.comboBox_t_4b, True)  # "True" enables the 20% tolerance band
        # Assign 5 Band
        attach_digit1(self.comboBox_1d_5b)
        attach_digit2(self.comboBox_2d_5b)
        attach_digit3(self.comboBox_3d_5b)
        attach_multiplier(self.comboBox_m_5b)
        attach_tolerance(self.comboBox_t_5b)
        # Assign 6 Band
        attach_digit1(self.comboBox_1d_6b)
        attach_digit2(self.comboBox_2d_6b)
        attach_digit3(self.comboBox_3d_6b)
        attach_multiplier(self.comboBox_m_6b)
        attach_tolerance(self.comboBox_t_6b)
        attach_tcr(self.comboBox_tcr_6b)
        # populate_combo_boxes

    def open_license(self):
        if self.license_window is None:
            self.license_window = LicenseAgreement()
        self.license_window.show()
