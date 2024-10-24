from time import time
import numpy as np
import yaml
import matplotlib.pyplot as plt

# Разные параметры из файла settings
with open('settings.yaml', encoding="utf8") as f:
    settings = yaml.safe_load(f)
    methods = settings["imports"]
    STEP = settings["STEP"]
    rendering_STEP = settings["rendering_STEP"]
    T_MIN, T_MAX = settings["T_MIN"], settings["T_MAX"]
    draw_graphs = settings["draw_graphs"]
    report_xyz = settings["report_xyz"]

# Временной диапазон(Массив чисел от T_MIN до T_MAX с шагом STEP)
t = np.arange(T_MIN, T_MAX, STEP)
t_r = np.arange(T_MIN, T_MAX, STEP * rendering_STEP)

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
        fig, ax = plt.subplots(4, 1, figsize=(10, 20))

        ax[0].plot(t_r, solution[:, 0], label='x(t)')
        ax[0].plot(t_r, solution[:, 1], label='y(t)')
        ax[0].plot(t_r, solution[:, 2], label='z(t)')
        ax[0].legend(loc='best')
        ax[0].set_xlabel('t')
        ax[0].set_ylabel('Concentration')
        ax[0].set_title('Concentrations(Time)')

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
        plt.savefig('tplot.png')

        plt.tight_layout()
        print("%6.2f сек." % (time() - start_graph_time))
        plt.show()

        input("Hit 'Return' to continue -> ")
