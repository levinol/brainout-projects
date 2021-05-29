# fandom-automation
Хелп тул для редакторов [фандома](https://brainout.fandom.com/ru/wiki/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0)
- [X] [files_to_string.py](files_to_string.py) работает
- [X] [lazy draggging system](https://github.com/levinol/fandom-automation/tree/master/lazydragging%20for%20alpha%20team) работает 
- [ ] [app.py](app.py) не работает

## files to string

**Для полноценной работы программы нужна копия папки _Weapons_ из оригинального кода проекта.**

В переменной ```path``` указываете **полный путь** к нужнему для вас оружию
```python
path = r'..\Weapons\mp7'
```
### Текущие проблемы и их решения:
- Название модификаций выводится на английском  - переведите
- Изображение модификаций выводится просто так - загрузите изображения сами
- Способ получения выводится чисто для понимания - замените
### Запуск программы 
1. Установите Python 3.6+ версии
2. Скачайте/скопируйте raw [files_to_string.py](files_to_string.py)
3. Откройте через стандартный IDLE для возможности изменения переменной ```path```
4. Запустите

## lazydragging for alpha team

Хелп тул для обновления билдов альфы 

[Собранный .exe файл](https://github.com/levinol/fandom-automation/blob/master/lazydragging%20for%20alpha%20team/dist/lazydragging.exe)
Для использования просто скачайте

[Основной python файл](https://github.com/levinol/fandom-automation/blob/master/lazydragging%20for%20alpha%20team/lazydragging.py)
Запускается из коробки, для запуска блида вручную запустите  

```>>>pyinstaller --onefile --icon=letto256.ico --noconsole lazydragging.py``` *(запускается из этой же директории)*

[Дизайнерский ui файл](https://github.com/levinol/fandom-automation/blob/master/lazydragging%20for%20alpha%20team/lazydragging_ui.ui)
Скелет дизайна собранный в qt designer, для конвертирования в .py файл запустите 

```>>>pyuic5 lazydragging_ui.ui -o lazydragging_ui.py```*(запускается из этой же директории)*

## app
Work in progress (Не трогайте) :wolf:
