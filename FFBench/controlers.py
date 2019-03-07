# pushbutton
self.pushbutton = QtWidgets.QPushButton('PushButton')

# checkable pushbutton
self.pushbutton_checkable = QtWidgets.QPushButton('PushButton (checkable)')
self.pushbutton_checkable.setCheckable(True)
self.pushbutton_checkable.setChecked(True)

# radiobutton
self.radiobutton = QtWidgets.QRadioButton('RadioButton')
self.radiobutton.setChecked(True)

# checkboxes
self.checkbox = QtWidgets.QCheckBox('CheckBox')
self.checkbox.setChecked(True)

# tristate checkbox
self.checkbox_tristate = QtWidgets.QCheckBox('Checkbox (tristate)')
self.checkbox_tristate.setTristate(True)

# combobox
self.combobox = QtWidgets.QComboBox()
self.combobox.addItems(['Item 1', 'Item 2', 'Item 3'])

# editable combobox
self.combobox_editable = QtWidgets.QComboBox()
self.combobox_editable.setEditable(True)
self.combobox_editable.addItems(['Item 1', 'Item 2', 'Item 3'])

# lineedit
self.lineedit = QtWidgets.QLineEdit('LineEdit')

# spinbox
self.spinbox = QtWidgets.QSpinBox()

# label
self.label = QtWidgets.QLabel('Label')

# horizontal scrollbar
self.hscrollbar = QtWidgets.QScrollBar(Qt.Horizontal)

# horizontal slider
self.hslider = QtWidgets.QSlider(Qt.Horizontal)

# LCD number
self.lcdnumber = QtWidgets.QLCDNumber()
self.lcdnumber.setNumDigits(10)
self.lcdnumber.display(1234567890)

# progressbar
self.progressbar = QtWidgets.QProgressBar()
self.progressbar.setValue(100)

# scrollarea
# pixmap = QtWidgets.QGraphicsPixmapItem(os.path.join('images', 'python_big_logo.png'))
# label = QtWidgets.QLabel()
# label.setPixmap(pixmap)
# self.scrollarea = QtWidgets.QScrollArea()
# self.scrollarea.setWidget(label)
# self.scrollarea.setAlignment(Qt.AlignCenter)

# groupbox
self.radiobutton1 = QtWidgets.QRadioButton('RadioButton 1')
self.radiobutton2 = QtWidgets.QRadioButton('RadioButton 2')
self.radiobutton3 = QtWidgets.QRadioButton('RadioButton 3')
groupbox_layout = QtWidgets.QVBoxLayout()
groupbox_layout.addWidget(self.radiobutton1)
groupbox_layout.addWidget(self.radiobutton2)
groupbox_layout.addWidget(self.radiobutton3)
self.groupbox = QtWidgets.QGroupBox('GroupBox')
self.groupbox.setLayout(groupbox_layout)

# checkable groupbox
self.checkbox1 = QtWidgets.QCheckBox('CheckBox 1')
self.checkbox2 = QtWidgets.QCheckBox('CheckBox 2')
self.checkbox3 = QtWidgets.QCheckBox('CheckBox 3')
groupbox_checkable_layout = QtWidgets.QVBoxLayout()
groupbox_checkable_layout.addWidget(self.checkbox1)
groupbox_checkable_layout.addWidget(self.checkbox2)
groupbox_checkable_layout.addWidget(self.checkbox3)
self.groupbox_checkable = QtWidgets.QGroupBox('GroupBox (checkable)')
self.groupbox_checkable.setLayout(groupbox_checkable_layout)
self.groupbox_checkable.setCheckable(True)

# toolbox
textedit = QtWidgets.QTextEdit('TextEdit')
plaintextedit = QtWidgets.QPlainTextEdit('PlainTextEdit')
self.toolbox = QtWidgets.QToolBox()
self.toolbox.addItem(textedit, 'Page 1')
self.toolbox.addItem(plaintextedit, 'Page 2')

# dial
self.dial = QtWidgets.QDial()

# vertical spacer on the left
vspacer_left = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)

# vertical spacer on the right
vspacer_right = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)

# vertical layout on the left
vlayout_left = QtWidgets.QVBoxLayout()
vlayout_left.addWidget(self.pushbutton)
vlayout_left.addWidget(self.pushbutton_checkable)
vlayout_left.addWidget(self.radiobutton)
vlayout_left.addWidget(self.checkbox)
vlayout_left.addWidget(self.checkbox_tristate)
vlayout_left.addWidget(self.combobox)
vlayout_left.addWidget(self.combobox_editable)
vlayout_left.addWidget(self.lineedit)
vlayout_left.addWidget(self.spinbox)
vlayout_left.addWidget(self.label)
vlayout_left.addWidget(self.hscrollbar)
vlayout_left.addWidget(self.hslider)
vlayout_left.addWidget(self.lcdnumber)
vlayout_left.addWidget(self.progressbar)
# vlayout_left.addWidget(self.scrollarea)
vlayout_left.addSpacerItem(vspacer_left)
# vlayout_left.setMargin(10)

# vertical layout on the right
vlayout_right = QtWidgets.QVBoxLayout()
vlayout_right.addWidget(self.groupbox)
vlayout_right.addWidget(self.groupbox_checkable)
vlayout_right.addWidget(self.toolbox)
vlayout_right.addWidget(self.dial)
vlayout_right.addSpacerItem(vspacer_right)
# vlayout_right.setMargin(10)

# horizontal layout
hlayout = QtWidgets.QHBoxLayout()
hlayout.addLayout(vlayout_left)
hlayout.addLayout(vlayout_right)
self.General_tab.setLayout = hlayout

# # central widget
central = QtWidgets.QWidget()
central.setLayout()
self.setCentralWidget(central)

# sets focus on QLineEdit widget and selects all the text
self.lineedit.setFocus()
self.lineedit.selectAll()