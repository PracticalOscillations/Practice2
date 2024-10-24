from time import time
import numpy as np
import matplotlib.pyplot as plt
import yaml


def method(f_x, f_y, f_z, w0: list, t: np.ndarray) -> np.ndarray:
    # Инициализируем массивы
    x = np.empty_like(t)
    y = np.empty_like(t)
    z = np.empty_like(t)
    # Разные данные
    x[0], y[0], z[0] = w0
    dt = t[1] - t[0]

    # метод Эйлера
    for i in range(1, t.shape[0]):
        
        x1 = x[i - 1] + dt * f_x(x[i - 1], y[i - 1], z[i - 1])
        y1 = y[i - 1] + dt * f_y(x[i - 1], y[i - 1], z[i - 1])
        z1 = z[i - 1] + dt * f_z(x[i - 1], y[i - 1], z[i - 1])

        dif_x = (f_x(x[i - 1], y[i - 1], z[i - 1]) + f_x(x1, y1, z1))/2
        dif_y = (f_y(x[i - 1], y[i - 1], z[i - 1]) + f_y(x1, y1, z1))/2
        dif_z = (f_z(x[i - 1], y[i - 1], z[i - 1]) + f_z(x1, y1, z1))/2
        
        x[i] = x[i - 1] + dt * dif_x
        y[i] = y[i - 1] + dt * dif_y
        z[i] = z[i - 1] + dt * dif_z

    solution = np.column_stack([x, y, z])
    return solution


if __name__ == "__main__":
    # Определяем функции системы уравнений
    def f_x(x, y, z):
        return -0.04 * x + 1e4 * y * z


    def f_y(x, y, z):
        return 0.04 * x - 1e4 * y * z - 3e7 * y ** 2


    def f_z(x, y, z):
        return 3e7 * y ** 2


    # Начальные условия
    x0 = 1.0
    y0 = 0.0
    z0 = 0.0
    w0 = [x0, y0, z0]

    # Разные параметры из файла settings
    with open('../settings.yaml', encoding="utf8") as f:
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

    # метод Эйлера
    start_init_time = time()
    print("Инициализация -------------------------> ", end="", flush=True)

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

        plt.tight_layout()
        print("%6.2f сек." % (time() - start_graph_time))
        plt.show()

    start_write_time = time()

    # Запись xyzt в файл xyzt.txt для дальнейшего использования
    if report_xyz:
        print("Запись в файл ------------------> ", end="", flush=True)
        np.savetxt(f'../results/xyzt_Euler_mod.txt', np.column_stack([solution, t_r]), fmt='%f')

        print("%6.2f сек." % (time() - start_write_time))
