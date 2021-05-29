# lazydragging for alpha team

Хелп тул для обновления билдов альфы 

[Собранный .exe файл](https://github.com/levinol/brainout-projects/blob/master/lazydragging%20for%20alpha%20team/build%20here/lazydragging.exe)
Для использования просто скачайте

[Основной python файл](https://github.com/levinol/brainout-projects/blob/master/lazydragging%20for%20alpha%20team/lazydragging.py)
Запускается из коробки, для запуска блида вручную запустите  

```>>>pyinstaller --onefile --icon=letto256.ico --noconsole lazydragging.py``` *(запускается из этой же директории)*

[Дизайнерский ui файл](https://github.com/levinol/brainout-projects/blob/master/lazydragging%20for%20alpha%20team/lazydragging_ui.ui)
Скелет дизайна собранный в qt designer, для конвертирования в .py файл запустите 

```>>>pyuic5 lazydragging_ui.ui -o lazydragging_ui.py```*(запускается из этой же директории)*
