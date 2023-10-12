import ipywidgets as widgets
from IPython import display as dsp
import random
import requests
import time
from IPython.display import clear_output
from ipywidgets import Button, HBox, Label, Output
from requests import Session
from IPython.display import display


class Bonus:

    def __init__(self, unique_id):
        self.unique_id = unique_id

        self.name = widgets.Text(
            value='',
            placeholder='Имя',
            description='Имя:',
            disabled=False
        )
        self.mail = widgets.Text(
            value='',
            placeholder='e-mail',
            description='e-mail:',
            disabled=False
        )
        self.phone = widgets.Text(
            value='',
            placeholder='телефон',
            description='Телефон:',
            disabled=False
        )
        # Кнопка Забронировать
        self.btn_access = widgets.Button(
            description='Забронировать',
            disabled=False,
            button_style='success',
            tooltip='Забронировать',
            icon='check'
        )
        # Кнопка Заново
        self.btn_reload = widgets.Button(
            description='Заново',
            disabled=False,
            button_style='warning',
            tooltip='Заново',
            icon='check'
        )
        # Кнопка Сохранить
        self.btn_send = widgets.Button(
            description='Сохранить',
            disabled=False,
            button_style='success',
            tooltip='Сохранить',
            icon='check'
        )

    def show_input_fields(self, btn_access):
        '''
        Функция, которая выводит поля для ввода
        '''

        self.label.close()
        self.buttons.close()

        display(self.name, self.mail, self.phone, self.btn_send)

    def btn_reload_clicked(self, btn_reload):
        '''
        Функция, которая крутит рулетку заново
        '''
        # Отчищаем поле вывода ячейки, чтобы там не копились прошлые бонусы
        dsp.clear_output(wait=True)

        # Очищаем все предыдущие обработчики событий.
        # Если не очистить, то нажатие на кнопку СОХРАНИТЬ отправит по запросу на каждый
        # созданный обработчик событий. Т.е. кол-во нажатий на заново + 1
        self.btn_send._click_handlers.callbacks = []
        # Новый обработчик событий нажатия на кнопку СОХРАНИТЬ
        self.btn_send.on_click(Bonus.post_bonus(self))

        # выбираем бонус
        names_dict = Bonus.get_bonus(self)

        # Выводим сообщения
        Bonus.show_bonuses(self, names_dict)

        # Нажатие на кнопки ЗАБРОНИРОВАТЬ и ЗАНОВО
        self.btn_access.on_click(self.show_input_fields)
        self.btn_reload.on_click(self.btn_reload_clicked)

    def get_bonus(self):
        # Получаем словарь с бонусами
        # session = requests.Session()
        # response = response = session.get('http://localhost:8000/random-bonus/', params={'unique_id': self.unique_id})
        # names_dict = response.json()
        names_dict = {
            'a': random.randint(1, 10),
            'b': random.randint(1, 10),
            'c': random.randint(1, 10)
        }
        return names_dict

    def post_bonus(self):
        # Отправляем в гугл таблицу
        # session = requests.Session()
        # response = response = session.post('http://localhost:8000/random-bonus/',
        # params={'name': self.name, 'phone': self.phone, 'email': self.email})
        def print_info(*args):
            print({'name': self.name.value, 'phone': self.phone.value, 'email': self.mail.value})

        return print_info

    def show_bonuses(self, names_dict):
        print('\033[1m' + 'Готовимся выбирать бонусы. . .' + '\033[0m')
        time.sleep(1.5)
        clear_output()

        # Создаем виджет для полосы загрузки
        progress = widgets.FloatProgress(value=0.0, min=0.0, max=1.0)

        for key, value in names_dict.items():
            # Выводим полосу загрузки и подпись под ней
            display(progress)
            print('Выбираем бонусы')

            # Обновляем полосу загрузки в течение 2 секунд
            for i in range(1, 21):
                time.sleep(0.2)
                progress.value = i / 20

            # Очищаем вывод
            clear_output()
            # Выводим бонус
            print('\033[1m' + '\033[92m' + 'Поздравляем! Ваш список бонусов:' + '\033[0m')
            print(f'- {key} ({value}руб.)')

        # Чистим все и выводим снова все бонусы сразу
        clear_output()
        print('\033[1m' + '\033[92m' + 'Поздравляем! Ваш список бонусов:' + '\033[0m')
        for key, value in names_dict.items():
            print(f'- {key} ({value}руб.)')

        # Считаем сумму всех бонусов и выводим
        total_bonus = sum(int(value) for value in names_dict.values())
        print('\033[4m' + f'\nВам выпало бонусов на {total_bonus} руб.\n' + '\033[0m')

        # Это принт, который можно потом стереть, не стирая все остальное.
        self.label = Label('\nВам нравится такой бонус?')
        # Две кнопки, расположенные рядом
        self.buttons = HBox([self.btn_access, self.btn_reload])
        # Отображаем принт и кнопки
        display(self.label, self.buttons)

    def start(self):
        # выбираем бонус
        names_dict = Bonus.get_bonus(self)

        # Выводим сообщения
        Bonus.show_bonuses(self, names_dict)

        # Обработчик событий нажатия на кнопку ЗАНОВО. При нажатии крутит рулетку заново
        self.btn_reload.on_click(self.btn_reload_clicked)

        # Обработчик событий нажатия на кнопку СОХРАНИТЬ. При нажатии на кнопку данные пользователя
        # и его бонус отправляются в гугл таблицу
        self.btn_send.on_click(Bonus.post_bonus(self))

        # Обработчик событий нажатия на кнопку ЗАБРОНИРОВАТЬ.
        # При нажатии показывает поля для ввода данных и кнопку СОХРАНИТЬ
        self.btn_access.on_click(self.show_input_fields)


Bonus('04d8f544-6c7e-4b9f-80c3-5a95b13acb4b').start()
