# Данные классов
classes = [
    {'name': '1-А', 'students': 20},
    {'name': '5-Б', 'students': 25},
    {'name': '10-В', 'students': 30},
]

# Данные студентов
students = [
    {'id': 1, 'first_name': 'Ибрагим', 'last_name': 'Ибрагимов', 'class': '10-Б'},
    {'id': 2, 'first_name': 'Мария', 'last_name': 'Петрова', 'class': '5-Б'},
    {'id': 3, 'first_name': 'Алексей', 'last_name': 'Сидоров', 'class': '10-В'},
]

# Данные предметов
subjects_data = {
    'Русский язык': [
        {'exam_topic': 'Орфография', 'exam_date': '2024-02-10', 'grade': '5', 'scan_url': '/static/scans/russian_test.pdf'},
        {'exam_topic': 'Синтаксис', 'exam_date': '2024-03-01', 'grade': '4', 'scan_url': '/static/scans/russian_syntax.pdf'},
    ],
    'Математика': [
        {'exam_topic': 'Тригонометрия', 'exam_date': '2024-02-20', 'grade': '3', 'scan_url': '/static/scans/math_trig.pdf'},
        {'exam_topic': 'Логарифмы', 'exam_date': '2024-03-05', 'grade': '5', 'scan_url': '/static/scans/math_log.pdf'},
    ],
    'История': [
        {'exam_topic': 'Реформация', 'exam_date': '2024-01-15', 'grade': '4', 'scan_url': '/static/scans/history_ref.pdf'},
        {'exam_topic': 'Наполеон', 'exam_date': '2024-02-25', 'grade': '5', 'scan_url': '/static/scans/history_nap.pdf'},
        {'exam_topic': 'Битва при Аустерлице', 'exam_date': '2024-03-01', 'grade': '5', 'scan_url': '/static/scans/history_nap.pdf'},
        {'exam_topic': 'ВОВ, ее участники', 'exam_date': '2024-03-21', 'grade': '5', 'scan_url': '/static/scans/history_nap.pdf'},
        {'exam_topic': 'Первый полет в космос', 'exam_date': '2024-04-17', 'grade': '4', 'scan_url': '/static/scans/history_nap.pdf'},
        {'exam_topic': 'Развал СССР', 'exam_date': '2024-05-22', 'grade': '---', 'scan_url': '/static/scans/history_nap.pdf'},
    ],
}

# Данные для student_panel
student_subjects = [
    {'name': 'Математика', 'teacher': 'Ислам Вахаевич', 'grade': '4'},
    {'name': 'История', 'teacher': 'учитель4', 'grade': '5'},
    {'name': 'Русский язык', 'teacher': 'учитель3', 'grade': '3'},
    {'name': 'Обществознание', 'teacher': 'учитель2', 'grade': '3'},
    {'name': 'Литература', 'teacher': 'учитель1', 'grade': '3'},
    {'name': 'Информатика', 'teacher': 'Иса', 'grade': '3'},

]