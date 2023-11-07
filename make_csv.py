# Сайт https://nomads.ncep.noaa.gov/gribfilter.php?ds=gdas_0p25 - доступны метео-данные в формате *.grib2
# Для чтения данного формата используется библиотека pygrib
# Часть программы, которая получает данные с сайта пропущена, исходные данные для анализа - см. файл C:/data_grib/tmp.grib2
# В полученном датасете - 4 координатные точки, наиболее близкие к анализируемой точке (шаг сетки данных - 0,25 градуса)
# Широта и долгота - [ 60.0 / 29.0 ] [ 60.0 / 29.25 ] [ 60.25 / 29.0 ] [ 60.25 / 29.25 ]
# U component of wind - широтная составляющая ветра (м/с)
# V component of wind - меридиональная составляющая ветра (м/с)
# Temperature - температура (Кельвин)
# Формат grbs[i] - <class 'pygrib._pygrib.gribmessage'> - включат в себя массивы numpy
# Т.е. формат grbs[i].values - <class 'numpy.ndarray'>
# Т.е. формат msg_t.values (msg_u.values, msg_v.values) - <class 'numpy.ndarray'>


import pygrib
import numpy as np
import pandas as pd
import math

# Данные по высотам в grib-файлах даются в виде стандартных уровней давления (50000 - 100000 Ра)
# Получив, при этом, данные о давлении на уровне моря можно пересчитать высоты в привычные единицы (метры)
# Функция H_t это и делает
H = 0
def H_t(t, p, p0):
    global H
    H = -29.21 * t * math.log(p / p0)
    return H


file = 'C:/data_grib/tmp.grib2'         # Исходные данные
grbs = pygrib.open(file)

# Распечатываем все сообщения выбранного датасета для контроля на стадии отладки программы.
# Потом этот блок можно убрать
for grb in grbs:
    print(grb)

msg = grbs[1]
coord_vals = msg.latlons()
print("[hp]", "[", coord_vals[0][0, 0], "/", coord_vals[1][0, 0], "]", "[", coord_vals[0][0, 1], "/", coord_vals[1][0, 1], "]", "[", coord_vals[0][1, 0], "/", coord_vals[1][1, 0], "]", "[", coord_vals[0][1, 1], "/", coord_vals[1][1, 1], "]")

msg_prmsl = grbs[1]
msg_prmsl_vals = msg_prmsl.values
prmsl_1 = float(msg_prmsl.values[0, 0])     #Pressure on sea level
prmsl_2 = float(msg_prmsl.values[0, 1])
prmsl_3 = float(msg_prmsl.values[1, 0])
prmsl_4 = float(msg_prmsl.values[1, 1])

huv = np.zeros((14, 13))
for i in range(1, 14):
    msg = grbs[3*i-1]
    p: int = str(msg).find('Pa:fcst')
    huv[i - 1, 0] = float(str(msg)[p-7:p-1])

for i in range(1, 14):
    msg_t = grbs[3 * i - 1]
    msg_u = grbs[3 * i]
    msg_v = grbs[3 * i + 1]
    temp_t_vals = msg_t.values
    temp_u_vals = msg_u.values
    temp_v_vals = msg_v.values
    t_klv = float(temp_t_vals[0, 0])
    p = huv[i - 1, 0]
    huv[i - 1, 1] = float(H_t(t_klv, p, prmsl_1))       # Уровни давления пересчитываем в высоту (метры)
    huv[i - 1, 2] = float(temp_u_vals[0, 0])
    huv[i - 1, 3] = float(temp_v_vals[0, 0])

for i in range(1, 14):
    msg_t = grbs[3 * i - 1]
    msg_u = grbs[3 * i]
    msg_v = grbs[3 * i + 1]
    temp_t_vals = msg_t.values
    temp_u_vals = msg_u.values
    temp_v_vals = msg_v.values
    t_klv = float(temp_t_vals[0, 1])
    p = huv[i - 1, 0]
    huv[i - 1, 4] = float(H_t(t_klv, p, prmsl_1))
    huv[i - 1, 5] = float(temp_u_vals[0, 1])
    huv[i - 1, 6] = float(temp_v_vals[0, 1])

for i in range(1, 14):
    msg_t = grbs[3 * i - 1]
    msg_u = grbs[3 * i]
    msg_v = grbs[3 * i + 1]
    temp_t_vals = msg_t.values
    temp_u_vals = msg_u.values
    temp_v_vals = msg_v.values
    t_klv = float(temp_t_vals[1, 0])
    p = huv[i - 1, 0]
    huv[i - 1, 7] = float(H_t(t_klv, p, prmsl_1))
    huv[i - 1, 8] = float(temp_u_vals[1, 0])
    huv[i - 1, 9] = float(temp_v_vals[1, 0])

for i in range(1, 14):
    msg_t = grbs[3 * i - 1]
    msg_u = grbs[3 * i]
    msg_v = grbs[3 * i + 1]
    temp_t_vals = msg_t.values
    temp_u_vals = msg_u.values
    temp_v_vals = msg_v.values
    t_klv = float(temp_t_vals[1, 1])
    p = huv[i - 1, 0]
    huv[i - 1, 10] = float(H_t(t_klv, p, prmsl_1))
    huv[i - 1, 11] = float(temp_u_vals[1, 1])
    huv[i - 1, 12] = float(temp_v_vals[1, 1])

print(huv)          # Тип данных <class 'numpy.ndarray'>

df = pd.DataFrame(data=huv)
np.savetxt('C:\data_grib\wdir.csv', df, delimiter=',', header='P,H1,UGRD1,VGRD1,H2,UGRD2,VGRD2,H3,UGRD3,VGRD3,H4,UGRD4,VGRD4')   # Сохраняем данные в файл *.csv
