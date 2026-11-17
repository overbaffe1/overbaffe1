# На обороте обложки

[← В альбом](../README.md)

**Марка и модель — две разные вещи.** Маяк на конверте — [векторная гравюра](../art/lighthouse.svg) по мотивам «Трёх чудес». А [маяк, который можно вращать](lighthouse.stl), — геометрия непосредственно из [модели MyWorkAiBrain](https://github.com/overbaffe1/MyWorkAiBrain/blob/83887965b2a98b5875a20dd4762a75758ba2e5ac/presentations/wow/models/glb/lighthouse.glb), в исходной позе. У STL нет материалов и анимации; прозрачное стекло и световые конусы убраны, чтобы не закрывать фонарь. Это экспонат для просмотра, не заготовка для 3D-печати. Миниатюра рядом с рассказом — уменьшенный [рендер той же сцены](https://github.com/overbaffe1/MyWorkAiBrain/blob/83887965b2a98b5875a20dd4762a75758ba2e5ac/presentations/wow/models/rasters/lighthouse-6516a9f808.png).

**Ещё два оттиска.** Координаты кристалла взяты из [текстового STL в gitEdit](https://github.com/overbaffe1/gitEdit/blob/main/atlas/samples/crystal.stl). Номера на билетах — не данные пассажиров, а пара из [теста Guardian-of-Truth](https://github.com/overbaffe1/Guardian-of-Truth/blob/7def70e18a9b3398536575eb3245c97877362089/tests/test_signals.py#L50-L59).

## Как перепечатать

Для просмотра ничего запускать не нужно. Чтобы изменить вёрстку, отредактируй [макет](../tools/print_album.py) или [рисунок](../art/lighthouse.svg). Из корня репозитория одна команда на Python 3 обновит две компоновки обложки, каждую в подвижной и неподвижной версиях:

```sh
python3 tools/print_album.py
```

На телефоне выбирается компактная композиция. По умолчанию `<picture>` загружает неподвижный рисунок; только при `prefers-reduced-motion: no-preference` луч совершает один короткий проход и замирает. Внешних шрифтов, счётчиков и сервисов картинок нет.

Для повторного экспорта STL скачай ровно ту ревизию GLB, по которой сделан альбом. Скрипт проверяет её SHA-256 и использует только стандартную библиотеку Python:

```sh
gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/overbaffe1/MyWorkAiBrain/contents/presentations/wow/models/glb/lighthouse.glb?ref=83887965b2a98b5875a20dd4762a75758ba2e5ac' > /tmp/lighthouse.glb
python3 tools/export_lighthouse.py /tmp/lighthouse.glb
```

## Почему альбом появится в профиле

Здесь применён [приём из gitEdit](https://github.com/overbaffe1/gitEdit/blob/main/atlas/surfaces.md#профиль-организация-репозиторий): GitHub показывает в профиле непустой корневой `README.md` из ветки по умолчанию публичного репозитория `логин/логин`. Для `overbaffe1/overbaffe1` это `main`. Название *портфолио* меняется в тексте — имя репозитория нужно оставить. Включать Pages или Actions не требуется.
