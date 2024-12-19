ymaps.ready(init_sp);
ymaps.ready(init_rd);
ymaps.ready(init_lp);
ymaps.ready(init_cp);
ymaps.ready(init_pd);
ymaps.ready(init_pa);


// Слонпаркет
const sp = [
["Магазин на Малом пр. ВО", "Малый пр-кт Васильевского острова, 52", 59.94298645857383, 30.26087979762224],
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 16 модуль", 59.852458257263535, 30.283748424922827],
["Магазин на Бухарестской", "Фучика улица, дом 9, ТК «Кубатура», 1 этаж, секция 1.72", 59.87576203827088, 30.368345705485666],
["Магазин на Удельной", "Энгельса проспект, дом 48, Слонпаркет", 60.012273082982, 30.323798834987564],
["Магазин на Гражданском", "Гражданский проспект, дом 15, к. 1", 60.00296850213114, 30.388395907113132],
["Магазин в ТЦ «Ланской»", "Студенческая улица, дом 10, ТК «Ланской», секция 20", 59.98937750356762, 30.327289041663803],
["Магазин на Железноводской", "Железноводская улица, дом 3, ТК «Василеостровский», 1 этаж, секция 20", 59.952925, 30.257630],
["Магазин на Старой Деревне", "Полевая Сабировская улица, дом 54, ТК \"Интерио\", 2 этаж, секция 213", 59.99722820211125, 30.268499494237734]
];

function init_sp () {
    var myMap = new ymaps.Map("map_sp", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of sp) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

// Центр Паркета №1
const cp = [
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 1 модуль", 59.85260046369783, 30.283901401874463],
["Магазин на Бухарестской", "Фучика улица, дом 9, ТК «Кубатура», 1 этаж, секция 1.74", 59.876030, 30.368932],
["Магазин на Старой Деревне", "Полевая Сабировская улица, дом 54, ТК «Интерио», 2 этаж, секция 212", 59.997190, 30.268518],
["Магазин на Удельной", "Энгельса проспект, дом 48А", 60.01218020875894, 30.323840116613678],
["Магазин на Уральской", "ул. Уральская, д. 10, ТЦ \"Василеостровский\", 1 этаж, секция 83", 59.952808064146836, 30.257612499999986],
];

function init_cp () {
    var myMap = new ymaps.Map("map_cp", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of cp) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

// Паркет 17 | 03
const pa = [
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 8-9 модуль", 59.85251549846404, 30.28357064782995],
["Магазин в ТЦ «Ланской»", "Студенческая улица, дом 10, ТК «Ланской», секция А1", 59.989270, 30.327627]
];

function init_pa () {
    var myMap = new ymaps.Map("map_pa", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of pa) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

// Ленплитка
const lp = [
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 2-3 модуль", 59.852747974396195, 30.28339697617016],
["Магазин на Удельной", "Энгельса проспект, дом 48", 60.012124468000856, 30.323818242724393],
["Магазин на Железноводской", "ул. Железноводская, д.3, ТЦ \"Василеостровский\", 2 этаж, секция 102", 59.95293044527378, 30.258059653442373]
];

function init_lp () {
    var myMap = new ymaps.Map("map_lp", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of lp) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

// Profildoors
const pd = [
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 13 модуль", 59.85261525638375, 30.283787585109],
];

function init_pd () {
    var myMap = new ymaps.Map("map_pd", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of pd) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

// Настоящие двери
const rd = [
["Магазин на Ленинском", "Ленинский проспект, дом 140А, ТЦ «Загородный дом 2», 4 модуль", 59.85260084595861, 30.283901230091026],
["Магазин на Удельной", "Энгельса проспект, дом 48, ЦВД", 60.012160389754854, 30.32379812615678],
["ТК «Василеостровский»", "Железноводская ул, дом 3, ТК «Василеостровский», секция 40", 59.952889, 30.258114]
];

function init_rd () {
    var myMap = new ymaps.Map("map_rd", {
            center: [59.93, 30.31],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        });

    for (let shop of rd) {
        myPlacemark = new ymaps.Placemark([shop[2], shop[3]], {
            // Чтобы балун и хинт открывались на метке, необходимо задать ей определенные свойства.
            balloonContentHeader: shop[0],
            balloonContentBody: shop[1],
            balloonContentFooter: "",
            hintContent: shop[0]
        })

        myMap.geoObjects.add(myPlacemark);
    }
}

