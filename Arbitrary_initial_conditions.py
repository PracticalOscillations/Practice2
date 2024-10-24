from time import time
import numpy as np
import yaml
import matplotlib.pyplot as plt
from random import random

# Разные параметры из файла settings
with open('settings.yaml', encoding="utf8") as f:
    settings = yaml.safe_load(f)
    methods = settings["imports"]
    STEP = settings["STEP"]
    rendering_STEP = settings["rendering_STEP"]
    T_MIN, T_MAX = settings["T_MIN"], settings["T_MAX"]
    draw_graphs = settings["draw_graphs"]
    report_xyz = settings["report_xyz"]

# Определяем функции системы уравнений
def f_x(x, y, z):
    return -0.04 * x + 1e4 * y * z


def f_y(x, y, z):
    return 0.04 * x - 1e4 * y * z - 3e7 * y ** 2


def f_z(x, y, z):
    return 3e7 * y ** 2


# Временной диапазон(Массив чисел от T_MIN до T_MAX с шагом STEP)
t = np.arange(T_MIN, T_MAX, STEP)
t_r = np.arange(T_MIN, T_MAX, STEP * rendering_STEP)

j = 1
while j <= 100:
    def random3():
        # Генерируем три случайных числа
        num1 = random()
        num2 = random()
        num3 = random()

        # Вычисляем их сумму
        sum_nums = num1 + num2 + num3

        # Нормализуем числа так, чтобы их сумма равнялась 1
        num1 /= sum_nums
        num2 /= sum_nums
        num3 /= sum_nums

        return [num1, num2, num3]

    w0 = random3()
    x0 = w0[0]
    y0 = w0[1]
    z0 = w0[2]
    print(f"Попытка №{j}. Рандомные начальные значения: {x0}, {y0}, {z0}")
    for i, p in methods.items():
        if p:
            print("=======================================================")
            print(f"Начало работы с полиэдром '{i}'")
            start_init_time = time()
            print("Инициализация -------------------------> ", end="", flush=True)

            exec(f'from methods.{i} import method')

            start_solve_time = time()
            print("%6.2f сек." % (start_solve_time - start_init_time))
            print("Расчет ---------------------------> ", end="", flush=True)

            solution = method(f_x, f_y, f_z, w0, t)[::rendering_STEP]

            start_graph_time = time()
            print("%6.2f сек." % (start_graph_time - start_solve_time))

            # Построим графики
            if draw_graphs:
                print("Постройка графика --------------> ", end="", flush=True)
                fig, ax = plt.subplots(4, 1, figsize=(10, 20))

                ax[0].plot(t_r, solution[:, 0], label='x(t)')
                ax[0].plot(t_r, solution[:, 1], label='y(t)')
                ax[0].plot(t_r, solution[:, 2], label='z(t)')
                ax[0].legend(loc='best')
                ax[0].set_xlabel('t')
                ax[0].set_ylabel('Concentration')
                ax[0].set_title(f'Concentrations(Time). Initial_conditions: {x0}, {y0}, {z0}')

                ax[1].plot(solution[:, 0], solution[:, 1])
                ax[1].set_xlabel('y')
                ax[1].set_ylabel('x')
                ax[1].set_title('x(y)')

                ax[2].plot(solution[:, 1], solution[:, 2])
                ax[2].set_xlabel('z')
                ax[2].set_ylabel('y')
                ax[2].set_title('y(z)')

                ax[3].plot(solution[:, 0], solution[:, 2])
                ax[3].set_xlabel('x')
                ax[3].set_ylabel('z')
                ax[3].set_title('z(x)')

                # Сохранение графика в файле
                plt.savefig(f'images/plot{j}.png')

                # Разделение данных на x, y и z координаты
                x = solution[:, 0]
                y = solution[:, 1]
                z = solution[:, 2]

                # Создание объекта для 3D графика
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                # Построение графика
                ax.scatter(x, y, z)

                # Установка меток осей
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')

                # Сохранение графика в файле
                plt.savefig(f'images3D/plot{j}.png')

                print("%6.2f сек." % (time() - start_graph_time))

    j += 1
