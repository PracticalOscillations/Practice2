from time import time
import matplotlib.pyplot as plt
import numpy as np
import yaml

# Разные параметры из файла settings
with open('settings.yaml', encoding="utf8") as f:
    settings = yaml.safe_load(f)
    methods = settings["imports"]
    STEP = settings["STEP"]
    rendering_STEP = settings["rendering_STEP"]
    T_MIN, T_MAX = settings["T_MIN"], settings["T_MAX"]
    draw_graphs = settings["draw_graphs"]
    report_xyz = settings["report_xyz"]

for i, p in methods.items():
    if p:
        print("=======================================================")
        print(f"Начало построения графика '{i}'")
        # Импортируем результаты
        print("Считываем из файла ------------------> ", end="", flush=True)
        start_read_time = time()
        with open(f'results/xyzt_{i}.txt') as f:
            solution = np.loadtxt(f)

        start_graph_time = time()
        print("%6.2f сек." % (start_graph_time - start_read_time))

        # Построим графики
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
        plt.savefig('3dplot.png')

        # Показать график
        print("%6.2f сек." % (time() - start_graph_time))
        plt.show()

        input("Hit 'Return' to continue -> ")
