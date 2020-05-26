import time
from src.Genetic_algorithm import *
from src.Full_search_algorithm import *
from math import *

genes_number = ["абвгдеёжзийклмнопрстуфхцчшщъыьэюя ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-.,!:;?«»— ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТ"
                "УФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "]

words = ["чушь", "ценА", ("А, почтеннейший! Вот и вы... в наших краях...  —  начал "
        "Порфирий, протянув ему обе руки. — Ну, садитесь-ка, батюшка!"),
         " Сходил на интересный blockbuster"]

if __name__ == "__main__":
    num = 3
    print("\nWORD: ", words[num], "\nLENGTH: ", len(words[num]))
    init_time = time.perf_counter()
    make_genetic_algorithm(words[num], genes_number[num])
    # full_search(genes_number[num], words[num])
    print("время выполнения: ", round(time.perf_counter() - init_time, 4))
