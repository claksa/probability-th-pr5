import math

import matplotlib.pyplot as plt
import numpy as np


def print_array(a):
    print(*a)


def calcs_var_series(a):
    print('Вариационный ряд')
    print_array(a)
    print(f'Первая порядковая статистика: {a[0]}')
    print(f'N-я порядковая статистика: {a[-1]}')
    print(f'Размах выборки: {a[-1]-a[0]}')


def calc_all(a):
    sample_set = sorted( list(set(a)) )
    frequencies = [a.count(set_item) for set_item in sample_set]
    sample_size = sum(frequencies)
    print(f'Объём выборки: {sample_size}')
    relative_frequencies = [frequencies[i] / sample_size for i in range(len(frequencies))]

    cumsum_arr = np.cumsum(frequencies)
    emp = [cumsum_arr[i]/sample_size for i in range(len(cumsum_arr))]

    print('Эмпирическая функция распределения:')
    prev = 0
    print(f'F*(x) = {0} при x <= {sample_set[prev]} ')
    for i in range(len(sample_set)):
        prev = i
        if prev+1 == len(sample_set):
            break
        print(f'F*(x) = {emp[i]} при {sample_set[prev]} < x <= {sample_set[prev+1]}')
    print(f'F*(x) = {1} при x >= {sample_set[-1]}')
    e_x = np.linspace(sample_set[0] - 0.5, sample_set[-1] + 0.5, 1000)
    e_y = [emp_func(i, sample_set, relative_frequencies) for i in x]

    m = math.ceil(1 + math.log2(len(sample_set)))
    h = (sample_set[-1] - sample_set[0]) / m
    x = [sample_set[0]+h*i for i in range(m)]
    y = [(emp_func(sample_set[0] + h * (i + 1)+0.001, sample_set, relative_frequencies) -
              emp_func(sample_set[0] + h * (i-0.001), sample_set, relative_frequencies))/h for i in range(m)]


    #интервальный ряд x_i -- середина интервала, n_i -- соотв. частоты
    avrg_x_arr = [0 for i in range(m)]
    freq_arr = [0 for i in range(m)]
    print('Интервальный ряд: ')
    for i in range(m):
        cur = sample_set[0] + h*i
        next = sample_set[0] + h*(i+1)
        print(f'Интервал: [{cur}; {next}]')
        avrg_x = (abs(next)-abs(cur))/2
        avrg_x_arr[i] = avrg_x
        cur_freq = emp_func(avrg_x, sample_set, relative_frequencies)
        freq_arr[i] = cur_freq
        print(f'x_i среднее: {avrg_x}, частость: {cur_freq}')


    #мат.ожидание
    exp_val = 0
    for i in range(len(frequencies)):
        exp_val += sample_set[i]*relative_frequencies[i]
    print(f'Выборочное среднее: {exp_val}')

    #дисперсия
    s = 0
    for i in range(len(frequencies)):
        s += sample_set[i]*sample_set[i]*relative_frequencies[i]
    dispersion = s - exp_val*exp_val
    print(f'Дисперсия: {dispersion}')
    corr_disp = len(sample_set)*dispersion/(len(sample_set)-1)
    print(f'Исправленная выборочная дисперсия: {corr_disp}')

    print(f'Среднее квадратичное отклонение: {math.sqrt(dispersion)}')
    print(f'Исправленное среднее квадратичное отклонение: {math.sqrt(corr_disp)}')

    #эмпирическая функция распределения
    plt.plot(e_x, e_y)
    plt.show()

    # гистограмма
    plt.bar(x, freq_arr, width=0.5)
    plt.show()

    # полигон
    plt.plot(x, freq_arr, ':o')
    plt.show()


def emp_func(x, my_set, rel_freq):
    sum = 0
    for i in range(len(my_set)):
        if my_set[i] < x:
            sum += rel_freq[i]
    return sum


if __name__ == '__main__':
    initial_sample = [0.92, -1.05, 1.04, 1.55, 0.92, -0.49, 1.49, 0.40, -0.61, 0.13,
                      0.51, -1.41, -1.03, -0.17, 0.17, -0.25, -1.48, 0.64, 0.43, 0.91]
    var_series = sorted(initial_sample)
    calcs_var_series(var_series)
    calc_all(var_series)



