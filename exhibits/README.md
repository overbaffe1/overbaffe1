# На обороте обложки

[← В альбом](../README.md)

**Марка и модель — две разные вещи.** Маяк на конверте — [векторная гравюра](../art/lighthouse.svg) по мотивам «Трёх чудес». А [маяк, который можно вращать](lighthouse.stl), — геометрия непосредственно из [модели MyWorkAiBrain](https://github.com/overbaffe1/MyWorkAiBrain/blob/83887965b2a98b5875a20dd4762a75758ba2e5ac/presentations/wow/models/glb/lighthouse.glb), в исходной позе. У STL нет материалов и анимации; прозрачное стекло и световые конусы убраны, чтобы не закрывать фонарь. Это экспонат для просмотра, не заготовка для 3D-печати. Миниатюра рядом с рассказом — уменьшенный [рендер той же сцены](https://github.com/overbaffe1/MyWorkAiBrain/blob/83887965b2a98b5875a20dd4762a75758ba2e5ac/presentations/wow/models/rasters/lighthouse-6516a9f808.png).

**Лист 02.** Координаты кристалла взяты из [текстового STL в gitEdit](https://github.com/overbaffe1/gitEdit/blob/main/atlas/samples/crystal.stl).

## Марки хакатонов

Как у [марок в gitEdit](https://github.com/overbaffe1/gitEdit#марки-вместо-меню), рисунок движется, а подпись остаётся на месте. У каждой марки два отдельных SVG: петля и её первый кадр. `<picture>` выбирает петлю только при `prefers-reduced-motion: no-preference`.

Номера закреплены за марками, а листы — за событиями. Поэтому № 07 (QAOA) стоит на отдельном листе [AI Challenge](https://aiijc.com/ru/about).

- **10 / AUSG.** На шкале — окна связи из учебной [смены P01_intro](https://github.com/overbaffe1/AUSG/blob/3f5232e75f3ea9dc7bcdf076c78067e3f9ee8436/data/P01_intro.json): первые 12 шагов `downlink_available` для S01, S02, S03, S04, S12, S13 и S16. Антенна — иллюстрация, не траектория реального аппарата.
- **11 / OMLP.** Шторка в атласе сравнивает две панели [одного чипа BS_tr_000095](https://github.com/overbaffe1/OMLP/blob/1a4aa4a40c62e6b5e06d3d1db4aa0c4e16094e7e/docs/figures/severity.png): индекс гари dNBR и ответ модели. В [сетке для печати](omlp-chip-95.json) 28 × 28 ячеек на панель: у индекса пять тонов по яркости рисунка, у ответа — преобладающий класс (0–3). Это миниатюра опубликованного сравнения, не новый прогноз.

[Скрипт печати](../tools/print_hackathons.py) собирает девять пар из корня альбома (Python 3.10+, без сети и внешних пакетов):

```sh
python3 tools/print_hackathons.py
```

## Архив иллюстраций

Ранние неподвижные иллюстрации и их исходные данные сохранены отдельно от галереи:

- **[03 / Два талона](../assets/trace-proof.svg).** Номера на билетах — пара из [теста Guardian-of-Truth](https://github.com/overbaffe1/Guardian-of-Truth/blob/7def70e18a9b3398536575eb3245c97877362089/tests/test_signals.py#L50-L59), не данные пассажиров.
- **[04 / Переписка](../assets/handoff-proof.svg).** Две стрелки — условный пример для [правила `deadlock`](https://github.com/overbaffe1/Coordination-Referee/blob/72593fec80e6d42e4046d29ca7d84e95838d8835/sol/localize.py#L78-L90), а не выдержка из чужого диалога. Правило получает класс сбоя на вход и определяет ход.
- **[05 / Контактный лист](../assets/frame-proof.svg).** Это чертёж в координатах [демокадра 256 × 256](https://github.com/overbaffe1/Vision-Action-Data-Factory/blob/afe7ed98c7f7db8efc27c06201b455788163a07a/data/final_input/libero_episode_0/frame_00000.jpg), не фотография робота. Рамки `[85,64,170,128]` и `[99,143,150,185]` взяты из автоматически составленной [аннотации](https://github.com/overbaffe1/Vision-Action-Data-Factory/blob/afe7ed98c7f7db8efc27c06201b455788163a07a/annotations.jsonl#L1-L4); четыре ярлыка — четыре записи об одном файле.
- **[06 / Перфолента](../assets/tempo-proof.svg).** Четыре отметки на каждой полосе — соседние строки одного плана. Во второй полосе расстояние между ними разделено на 1,3. Это временная шкала исполнения, **не** частота сетевых запросов: [в протоколе](https://github.com/overbaffe1/Green-Challenge/blob/5e27768309ef18f0422b218d5daee9f3778198f4/docs/ARCHITECTURE.md#why-the-request-rate-is-fixed) интервал запросов остаётся равным 80 мс.
- **[07 / Рельеф](../assets/qaoa-proof.svg).** Одна и та же сетка вероятностей напечатана краской и записана треугольниками в STL. [Рецепт ниже](#как-построен-рельеф).
- **[08 / Хронометр](../assets/latency-proof.svg).** Обе полосы начинаются с нуля. Их длины соответствуют `ref_neg_sec` и `fast_neg_1token_sec` из блока [`equivalence`](https://github.com/overbaffe1/3D-DIT-Distillation/blob/d65823d79066eb6e67a722d8a3db2f4153739ac7/fetched_info/solver_experiments.json#L2-L12). Это сохранённые замеры проекта, не новый запуск на GPU.
- **[09 / Запас](../assets/orbit-proof.svg).** Орбита — иллюстрация, но уровень на шкале взят из [строки планировщика](https://github.com/overbaffe1/CosmoH/blob/828e19eca78b6392da9610b2c04f20fcc199094a/solutions/fuel-contour/docs/evidence/balance-example.json): `inventory_t / capacity_t`, то есть 20,0144 из 70 т в конце первого дня.

## Как построен рельеф

Для [экспоната 07](qaoa-relief.stl) нужен один пример, а не весь датасет. В [паспорте задачи 0](qaoa-case-0.json) сохранены [матрица взаимодействий J](https://github.com/overbaffe1/QAOA/blob/a993143505f1889075c57f663c06c4f5a79722cc/J.npy), [первая строка массива h_train](https://github.com/overbaffe1/QAOA/blob/a993143505f1889075c57f663c06c4f5a79722cc/h_train.npy) и [десять углов строки id=0](https://github.com/overbaffe1/QAOA/blob/a993143505f1889075c57f663c06c4f5a79722cc/merged2.csv). Это срез [симулятора проекта](https://github.com/overbaffe1/QAOA/blob/a993143505f1889075c57f663c06c4f5a79722cc/QAOA.py), а не результат измерения на квантовом компьютере.

Первые четыре слоя неизменны. По оси X меняется `beta_4`, по Y — `gamma_4`, каждый на ±0,75 радиана вокруг значения из CSV. Для каждой из 25 × 25 точек посчитана суммарная вероятность состояний с минимальной энергией. В STL высота над нулём равна `1,5 + 66 × P`; 1,5 — толщина подложки. Точка на гравюре отмечает исходную пару: **P ≈ 0,46959**. Это локальный срез, не доказательство глобального максимума. Гребень хорошо заметен, если сдвинуть только один угол:

| Положение | P(ground) |
|---|---:|
| Центр | 0,469589 |
| На 0,75 рад дальше по `gamma_4` | 0,416731 |
| На 0,75 рад дальше по `beta_4` | 0,000059 |

Чтобы пересчитать модель и её миниатюру, из корня альбома на Python 3.10+:

```sh
python3 tools/print_relief.py
python3 -m unittest discover -s tests -v
```

Сеть, NumPy и веса моделей не нужны. Тест сверяет выбранные точки с прямым расчётом состояния и проверяет, что у сетки STL нет открытых рёбер.

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
