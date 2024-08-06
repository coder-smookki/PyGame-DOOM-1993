# PyGame-DOOM-1993

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/coder-smookki/PyGame-DOOM-1993/blob/main/LICENSE)
![Version Python](https://img.shields.io/badge/python-=>3.10-orange)
[![Stars](https://img.shields.io/github/stars/coder-smookki/PyGame-DOOM-1993?style=flat
)](https://github.com/coder-smookki/PyGame-DOOM-1993/stargazers)


## Как запускать проект?

1. `git clone https://github.com/coder-smookki/PyGame-DOOM-1993.git`

2. `python -m venv .venv`

3. `pip install -r requirements.txt`

4. `cd src` and `python main.py`

## Какие технологии присутствуют?

* Python 3.10

* PyGame

* Method Ray-Casting

* Net effect 2.5D

* Using Sprites
  
---

# Этапы разработки
    
## 1. Создание 2D модели игры
  
![Screenshot_1](https://user-images.githubusercontent.com/102893182/213878723-2d3f2266-9420-4207-a22c-f15f16eab3b4.png)

_На данном этапе был отрисован игрок, его направление и карта_
  
## 2. Алгоритм "ray casting"

![Screenshot_2](https://user-images.githubusercontent.com/102893182/213878741-686687ee-bb26-46d1-8d97-1057db4c1475.png)

_Реализован алгоритм ray casting, представляющий собой определенное количество лучей (область видимости игрока), сталкивающихся со стенами карты_
  
## 3. Проектирование 2.5D и отрисовка миникарты
  
![Screenshot_3](https://user-images.githubusercontent.com/102893182/213878757-6afd9e4e-fb26-480a-8162-b708ee088446.png)

## 4. Добавление текстур

![Screenshot_4](https://user-images.githubusercontent.com/102893182/213878775-e8d652e2-c339-4af2-a986-b49dc9579f36.png)

## 5. Добавление коллизий
  
![Screenshot_19](https://user-images.githubusercontent.com/102893182/213879761-c23299f0-75a8-4964-9f18-5db6906732b6.png)
  
_Были добавлены столкновения со стеной, чтобы игрок не входил в стены и за рамки карты_
  
## 6. Добавление оружий

![Screenshot_5](https://user-images.githubusercontent.com/102893182/213878790-b4517583-f184-4dd4-ac67-b0f4043f1376.png)

_Добавлена функция смены оружия при прокрутке колесика мыши, а также анимации каждого оружия_
  
## 7. Добавление звука

![Screenshot_20](https://user-images.githubusercontent.com/102893182/213879753-d2e1f640-17e4-4b18-b4d4-a0aa18f0f759.png)
  
_Была добавлена фоновая музыка, звуки шагов и выстрела оружия_
  
## 8. Добавление спрайтов врагов. Фиксация уровня жизни и количества потронов


![Screenshot_6](https://user-images.githubusercontent.com/102893182/213878801-f7f21cbe-e7ed-4b84-8158-d02426776b73.png)

## 9. Финальные окна с подсчетом очков

![Screenshot_7](https://user-images.githubusercontent.com/102893182/213878814-95271c34-3fc9-48aa-b20f-32076dc20d32.png)

![Screenshot_8](https://user-images.githubusercontent.com/102893182/213878817-cac2f79b-1a5c-4219-9cb6-8f8ce1aa8b65.png)

## 10. Добавление стартового окна с настройками и выбором уровней

![Screenshot_9](https://user-images.githubusercontent.com/102893182/213878834-03b7af7e-3064-455b-a5be-9f552de3d84c.png)

![Screenshot_10](https://user-images.githubusercontent.com/102893182/213878838-93f55a2a-a045-40c8-b466-0b254b45b4aa.png)

![Screenshot_11](https://user-images.githubusercontent.com/102893182/213878846-ccfd9aaf-bbca-4ddc-855e-7ace46648063.png)

---

# Смысл игры
    
_Игра DOOM является аналогом игры-шутера DOOM в 2.5D. В игре будет реализовано 5 уровней. Игра идет от первого лица. Игроку неободимо победить противника в перестрелке и попасть на новый уровень. Уровни отличаются сложностью карты (меньше укрытий), количеством врагов._
    
---
