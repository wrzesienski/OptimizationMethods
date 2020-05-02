import time
from Optim_Lab3.src.Genetic_algorithm import *

genes_number = ["абвгдеёжзийклмнопрстуфхцчшщъыьэюя ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-.,!:;?«»— ",
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТ"
                "УФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "]

words = ["чушь", "ценА", ("А, почтеннейший! Вот и вы... в наших краях...  —  начал "
        "Порфирий, протянув ему обе руки. — Ну, садитесь-ка, батюшка!"),
         " Сходил на интересный blockbuster"]

if __name__ == "__main__":
    num =1
    print("\nWORD: ", words[num], "\nLENGTH: ", len(words[num]))
    init_time = time.perf_counter()
    make_genetic_algorithm(words[num], genes_number[num])
    print("время выполнения: ", round((time.perf_counter()-init_time)/60, 4))