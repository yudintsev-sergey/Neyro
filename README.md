# Neyro
Создан на период учебы Data Science
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
