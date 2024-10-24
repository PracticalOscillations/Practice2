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

# Построим графики
fig, ax = plt.subplots(3, 1, figsize=(10, 20))

for p, i in enumerate(methods.keys()):
    if p == 0:
        print("=======================================================")
        # Импортируем результаты
        print("Считываем из файла идеальные результаты ------------------> ", end="", flush=True)
        start_read_time = time()
        with open(f'results/xyzt_{i}.txt') as f:
            solution0 = np.loadtxt(f)

        start_graph_time = time()
        print("%6.2f сек." % (start_graph_time - start_read_time))
    else:
        print("=======================================================")
        print(f"Начало построения графика '{i}'")
        # Импортируем результаты
        print("Считываем из файла ------------------> ", end="", flush=True)
        start_read_time = time()
        with open(f'results/xyzt_{i}.txt') as f:
            solution = np.loadtxt(f)

        start_graph_time = time()
        print("%6.2f сек." % (start_graph_time - start_read_time))
        print("Постройка графика --------------> ", end="", flush=True)

        # Добавим в график
        ax[0].plot(t_r, solution0[:, 0] - solution[:, 0], label=i)
        ax[0].legend(loc='best')
        ax[0].set_xlabel('t')
        ax[0].set_ylabel('x')
        ax[0].set_title('x(t)')

        ax[1].plot(t_r, solution0[:, 1] - solution[:, 1], label=i)
        ax[1].legend(loc='best')
        ax[1].set_xlabel('t')
        ax[1].set_ylabel('y')
        ax[1].set_title('y(t)')

        ax[2].plot(t_r, solution0[:, 2] - solution[:, 2], label=i)
        ax[2].legend(loc='best')
        ax[2].set_xlabel('t')
        ax[2].set_ylabel('z')
        ax[2].set_title('z(t)')

        plt.tight_layout()
        print("%6.2f сек." % (time() - start_graph_time))

# Сохранение графика в файле
plt.savefig(f'comparison_plot.png')


plt.show()
