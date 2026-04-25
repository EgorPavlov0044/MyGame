from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout
#from PyQt5.QtGui import QFont,  QPalette

from random import shuffle, choice, randint
from sys import exit
from threading import Thread



categories = [{"Geography": 
              {1: ("Какое озеро самое большое в мире?", ("Каспийское море",), 
                   ["Чудское озеро", "Озеро Верхнее", "Озеро Виктория", "Озеро Байкал", "Карское море", "Озеро Гурон"]),
                   2: ("Какая горная ситсмеа самая длинная в мире?", ("Анды",),
                       ["Гималаи", "Тибет", "Альпы", "Уральские горы", "Кордильеры", "Кавказ", "Эверест"]),
                       3: ("Какая река самая длинная в мире?", ("Амазонка",),
                           ["Нил", "Конго", "Янцзы", "Волга", "Обь", "Миссисипи", "Хуанхэ"]),
                           4: ("Сколько в мире существует океанов?", ("5",),
                               ["3", "4", "6", "7"]),
                               5: ("Какой остров самый большой в мире?", ("Гренландия",),
                                   ["Новая Гвинея", "Калимантан", "Великобритания", "Мадагаскар", "Суматра"])}, 
              "Biology": 
              {1: ("Как называется ткань растения, отвечающая за рост растения в толщину?", ("Камбий",),
                   ["Луб", "Склеренхима", "Пробка", "Ксилема"]),
                   2: ("Что не является органоидом растения?", ("Склеренхима", "Флоэма", "Эпидерма"),
                       ["Цитоплазма", "Вакуоль", "Ядро", "Аппарат Гольджи", "Лизосома", "Рибосома", "Клеточная мембрана", "Митохондрия"]),
                       3: ("Как называются одноклеточные животные?", ("Простейшие",),
                           ["Одноклеточные", "Инфузории", "Хордовые"]),
                           4: ("Как называются одноклеточные организмы, которые не имеют оформленного ядра?", ("Прокариоты", "Доядерные"),
                               ["Эукариоты", "Безъядерные", "Неядерные", "Простейшие", "Археи"]),
                               5: ("Как называется органоид клетки, запасающий вещества?", ("Вакуоль",),
                                   ["Митохондрия", "Ядро", "Эндоплазматическая сеть", "Цитоплазма", "Клеточная мембрана"]),},
              "History":    
              {1: ("Как звали третьего персидского царя?", ("Ксеркс",),
                   ["Ксерск", "Дарий", "Кир", "Леонид"]),
                   2: ("Как назывался древнегреческий сосуд для хранения вина и масла?", ("Амфора",),
                       ["Пифос", "Ваза", "Керамик", "Фидий"]),
                       3: ("Как называлась древнегреческая монета?", ("Драхма",),
                           ["Брахма", "Фоллис", "Солид", "Кератий"]),
                           4: ("Что не является одним из семи чудес света?", ("Великая Китайская стена", "Римский Колизей"),
                               ["Александрийский маяк", "Храм Артемиды Эфесской", "Колосс Родосский", "Висячие сады Семирамиды", "Статуя Зевса в Олимпии", "Пирамида Хеопса"]),
                               5: ("В каком году появились Олимпийские игры?", ("В 776 г. до н. э.",),
                                   ["В 997 г. до н. э.", "В 994 г. до н. э.", "В 976 г. до н. э.", "В 796 г. до н. э."])},
              },
              {"Geography":
              {1: ("Ватикан - самая маленькая страна в мире", True),
              2: ("Атлантический океан - 2 по размеру океан в мире", False),
              3: ("Большая часть России находится в Европе", False),
              4: ("Антропогенные объекты - объекты, созданные человеком", True),
              5: ("", True)}
              }]


right_answers = 0
wrong_answers = 0
answered = [False, False]
exit_signal = False
continue_signal = False
come_in = True
stage = 0
checked_buttons = [False]*4


def right_answer():
    global right_answers, answered, waiting
    answered = [True, True]
    right_answers += 1

def wrong_answer():
    global wrong_answers, answered, waiting 
    answered = [True, False]
    wrong_answers += 1 

def exit_message(): 
    global exit_signal
    exit_signal = True

def continue_message():
    global continue_signal
    continue_signal = True

#empty = lambda: None    



def task():
    while True:
        try:
            global answered, answer_text, right_answer_text, right_variant, exit_signal, continue_button, continue_signal, variant_buttons, checked_buttons
            while True:
                if answered[0]:
                    for i in range(len(variant_buttons)):
                        if variant_buttons[i].isChecked():
                            checked_buttons[i] = True

                    if answered[1]:
                        answer_text.setText("Правильно!")
                        answer_text.setStyleSheet("color:green")
                    else:
                        answer_text.setText("Неправильно!")
                        answer_text.setStyleSheet("color:red") 

                    right_answer_text.setText(f"Прав. ответ: {right_variant}")
                    answer_text.show()
                    right_answer_text.show()
                    continue_button.show()

                    answered = [False, False] 
            
                if continue_signal:
                    ask()
                    continue_signal = False
                else:
                    for i in range(len(checked_buttons)):
                        variant_buttons[i].setChecked(checked_buttons[i])
    

                if exit_signal: break    


        except: pass
        finally:
            if exit_signal: break



app = QApplication([])
signal = app.aboutToQuit.connect(exit_message)

screen = QWidget()
screen.show()
screen.setWindowTitle("AnswerCard")
screen.resize(600, 440)

a = QRadioButton()
b = QRadioButton()
c = QRadioButton()
d = QRadioButton()

variant_buttons = (a, b, c, d)
continue_button = QPushButton("Продолжить")

main_layout = QVBoxLayout()
question_layout = QHBoxLayout()
variant_group = QButtonGroup()
variant_layout = QVBoxLayout()
answer_layout = QHBoxLayout()

stat_text = QLabel()
category_text = QLabel()
question_text = QLabel()
answer_text = QLabel()
right_answer_text = QLabel()


for i in variant_buttons:
    variant_group.addButton(i)

main_layout.addLayout(question_layout)
#main_layout.addWidget(variant_group, alignment=Qt.AlignTop|Qt.AlignVCenter)
main_layout.addLayout(answer_layout)

question_layout.addWidget(category_text, alignment=Qt.AlignLeft|Qt.AlignTop)
question_layout.addWidget(question_text, alignment=Qt.AlignHCenter|Qt.AlignVCenter)
question_layout.addWidget(stat_text, alignment=Qt.AlignRight|Qt.AlignTop)

answer_layout.addWidget(answer_text, alignment=Qt.AlignLeft)
answer_layout.addWidget(continue_button, alignment=Qt.AlignHCenter)
answer_layout.addWidget(right_answer_text, alignment=Qt.AlignRight)



def ask():
    global checked_buttons, categories, variant_buttons, variants, right_variant, category_text, question_text, stat_text, continue_button, answer_text, right_answer_text

    for i in (continue_button, answer_text, right_answer_text): i.hide()

    variants = []

    category = choice(list(categories[0].keys()))
    question_number = randint(1, 5)
    question = categories[stage][category][question_number]

    right_variant = choice(question[1])
    variants.append(right_variant)
    for i in range(3):
        choosed_variant = choice(question[2])
        variants.append(choosed_variant)
        question[2].remove(choosed_variant)

    shuffle(variants)
    variant_group.setExclusive(False)
    for i in range(len(variant_buttons)):
        variant_buttons[i].setChecked(False)
        checked_buttons[i] = False
        variant_buttons[i].setText(variants[i])
    variant_group.setExclusive(True)    

    category_text.setText(f"1|{category}|{question_number}")
    question_text.setText(question[0]) 
    stat_text.setText(f"Прав.: {right_answers}\nНеправ.: {wrong_answers}")   

    del categories[stage][category][question_number]

    for i in range(len(variant_buttons)):
        if variant_buttons[i].text() == right_variant: variant_buttons[i].clicked.connect(right_answer)
        else: variant_buttons[i].clicked.connect(wrong_answer)

    


    continue_button.clicked.connect(continue_message)    


ask()

if come_in:
    th = Thread(target=task)
    th.start()
    come_in = False


    

screen.setLayout(main_layout)
exit(app.exec_())


