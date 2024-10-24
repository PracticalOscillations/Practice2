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
    x0 = random()
    y0 = random()
    z0 = random()
    w0 = [x0, y0, z0]
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
