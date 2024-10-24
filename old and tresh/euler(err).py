import numpy as np
import matplotlib.pyplot as plt


def euler_solver(dt, t_max):
    t = np.arange(0, t_max, dt)
    x = np.empty_like(t)
    y = np.empty_like(t)
    z = np.empty_like(t)
    x[0] = 1
    y[0] = 0
    z[0] = 0
    for i in range(1, t.shape[0]):
        x[i] = x[i-1] + dt*(-0.04*x[i-1] + 1e4*y[i-1]*z[i-1])
        y[i] = y[i-1] + dt*(0.04*x[i-1] - 1e4*y[i-1]*z[i-1] - 3e7*y[i-1]**2)
        z[i] = z[i-1] + dt*(3e7*y[i-1]**2)
    return x, y, z, t


# Решаем с двумя разными шагами
x1, y1, z1, t1 = euler_solver(dt=0.0002, t_max=1000)
x2, y2, z2, t2 = euler_solver(dt=0.0002/2, t_max=1000)

# Чтобы сравнить два решения, нам нужно интерполировать решение с меньшим шагом
x2_interp = np.interp(t1, t2, x2)
y2_interp = np.interp(t1, t2, y2)
z2_interp = np.interp(t1, t2, z2)

# Вычисляем ошибку
error_x = np.abs(x1 - x2_interp)
error_y = np.abs(y1 - y2_interp)
error_z = np.abs(z1 - z2_interp)

# Построение графиков ошибок
plt.figure(figsize=(12, 9))
plt.subplot(3, 1, 1)
plt.plot(t1, error_x, label='Error in x')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t1, error_y, label='Error in y')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t1, error_z, label='Error in z')
plt.legend()

plt.show()
