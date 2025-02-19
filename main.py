from tkinter import *
from tkinter import ttk, font
import random

from cramer_calc import solve_linear_system


def construct_matrix_entries() -> None:
    global matrix_frame, matrix_entries

    if matrix_frame is not None:
        matrix_frame.destroy()
        matrix_entries = []

    matrix_frame = Frame(highlightthickness=3, highlightbackground="black", highlightcolor='black')

    for row_num in range(matrix_size):
        matrix_entries.append([])
        for col_num in range(matrix_size + 1):
            entry = ttk.Entry(matrix_frame, justify=CENTER, font=font.Font(family="Consolas", size=16), width=10)
            matrix_entries[row_num].append(entry)

            if col_num == matrix_size:
                Frame(matrix_frame, width=3, background='black').grid(row=0, column=col_num,
                                                                      rowspan=matrix_size, sticky='ns', padx=5)
                col_num += 1

            entry.grid(row=row_num, column=col_num, ipady=20)

    matrix_frame.grid(row=2, sticky='w', columnspan=30)


def update_matrix_size_by(mod: int, construct_new_matrix=False) -> None:
    global matrix_size, size_label

    if size_label is None:
        size_label = ttk.Label(size_adjustment_frame, font=("Comic Sans MS", 16, "italic"))
        size_label.pack(side='left')

    if matrix_size + mod in range(1, 10):
        matrix_size += mod
        size_label['text'] = f'Размеры матрицы: {matrix_size} * {matrix_size + 1}'

        if construct_new_matrix:
            construct_matrix_entries()


def gen_random_values() -> None:
    for row in matrix_entries:
        for entry in row:
            if random.random() < 0.1:
                value = complex(random.randint(-20, 20), random.randint(1, 20) * random.choice([-1, 1]))
            else:
                value = random.randint(-20, 20)

            entry.delete(0, END)
            entry.insert(0, value)


def parse_complex_number(num: str) -> complex:
    value = num.replace(' ', '').replace('i', 'j').replace('(', '').replace(')', '')

    if value[-1] != 'j' and 'j' in value:
        j_index = value.index('j')
        if value[0] in ['-', '+']:
            value = value[j_index + 1:] + value[:j_index + 1]
        else:
            value = value[j_index + 1:] + "+" + value[:j_index + 1]

    return complex(value)


def get_answer() -> None:
    # Transform str-matrix into complex-matrix while trying to catch any possible errors
    final_matrix = []
    for row in matrix_entries:
        final_matrix.append([])

        has_error = False
        for entry in row:
            try:
                final_matrix[-1].append(parse_complex_number(entry.get()))
            except (ValueError, IndexError):
                answer_label['text'] = 'Введены некорректные данные!'
                has_error = True
                break

        if has_error:
            break
    else:
        # If no errors were found, try to solve the system
        result = solve_linear_system(final_matrix)

        if result is None:
            answer_label['text'] = 'Система несовместна.'
        else:
            text = 'Ответ: \n'
            for root_number in range(matrix_size):
                text += f'x{root_number + 1} = {result[root_number]}\n'

            answer_label['text'] = text


root = Tk()
root.title('Калькулятор СЛАУ')
root.geometry('1200x1100')
root.state('zoomed')

# Grid configuration

for i in range(5):
    root.rowconfigure(index=i, weight=1)
root.rowconfigure(index=5, weight=50)

# Upper label

label = ttk.Label(text='В ячейки введите коэффициенты линейных уравнений, а затем нажмите кнопку "Решить систему"',
                  font=("Comic Sans MS", 16, "bold", "underline"))
label.grid(row=0, sticky='w')

matrix_frame, size_label = None, None  # initially None 'cuz they are being replaced/updated later

# Matrix size label + adjustment buttons

size_adjustment_frame = Frame()
matrix_size = 3
update_matrix_size_by(0)

plus_button = Button(size_adjustment_frame, text='+', font=("Arial", 30,), padx=0, pady=0, width=3,
                     command=lambda: update_matrix_size_by(1, True))
minus_button = Button(size_adjustment_frame, text='-', font=("Arial", 30), padx=0, pady=0, width=3,
                      command=lambda: update_matrix_size_by(-1, True))
plus_button.pack(side='left', padx=10)
minus_button.pack(side='left')

size_adjustment_frame.grid(row=1, sticky='w')

# Matrix entries

matrix_entries = []
construct_matrix_entries()

# Lower buttons (generate random values + solve a system)

lower_buttons_frame = Frame()
gen_button = Button(lower_buttons_frame, text='Сгенерировать случайные значения', font=("Comic Sans MS", 16, "italic"),
                    command=gen_random_values)
solve_button = Button(lower_buttons_frame, text='Решить систему', font=("Comic Sans MS", 16, "italic"),
                      command=get_answer)

gen_button.pack(side='left', padx=10)
solve_button.pack(side='left')

lower_buttons_frame.grid(row=3, sticky='w')

# Answer label

answer_label = Label(font=("Consolas", 18), fg='red', justify=LEFT)
answer_label.grid(row=4, sticky='w')

# Main loop

root.mainloop()
