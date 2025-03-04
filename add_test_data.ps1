# Скрипт для добавления тестовых данных через API

$apiBaseUrl = "http://localhost:8000/api"

# Добавление новых категорий
$categories = @(
    @{
        name = "Архитектура"
        color = "#8A2BE2"
        description = "Важные архитектурные сооружения и стили"
    },
    @{
        name = "Спорт"
        color = "#32CD32"
        description = "Спортивные события и достижения"
    },
    @{
        name = "Технологии"
        color = "#00CED1"
        description = "Технологические инновации и изобретения"
    },
    @{
        name = "Религия"
        color = "#FFD700"
        description = "Религиозные события и движения"
    },
    @{
        name = "Исследования"
        color = "#4682B4"
        description = "Географические открытия и исследования"
    }
)

Write-Host "Добавление новых категорий..."
foreach ($category in $categories) {
    try {
        $response = Invoke-RestMethod -Uri "$apiBaseUrl/categories" -Method Post -Body ($category | ConvertTo-Json) -ContentType "application/json"
        Write-Host "Категория добавлена: $($response.name), ID: $($response.id)"
    }
    catch {
        Write-Host "Ошибка при добавлении категории $($category.name): $_"
    }
}

# Получаем все категории для определения их ID
$allCategories = Invoke-RestMethod -Uri "$apiBaseUrl/categories" -Method Get
$categoryLookup = @{}
foreach ($cat in $allCategories) {
    $categoryLookup[$cat.name] = $cat.id
}

# Добавление новых событий
$events = @(
    @{
        title = "Строительство Берлинской стены"
        date = "1961-08-13T00:00:00"
        end_date = "1989-11-09T00:00:00"
        description = "Возведение стены, разделившей Берлин на восточную и западную части"
        location = "Берлин, Германия"
        importance = 5
        category_id = $categoryLookup["Политика"]
    },
    @{
        title = "Падение Берлинской стены"
        date = "1989-11-09T00:00:00"
        description = "Разрушение Берлинской стены, символизирующее окончание Холодной войны"
        location = "Берлин, Германия"
        importance = 5
        category_id = $categoryLookup["Политика"]
    },
    @{
        title = "Строительство Эйфелевой башни"
        date = "1887-01-28T00:00:00"
        end_date = "1889-03-31T00:00:00"
        description = "Строительство одной из самых известных достопримечательностей в мире"
        location = "Париж, Франция"
        importance = 3
        category_id = $categoryLookup["Архитектура"]
    },
    @{
        title = "Олимпийские игры в Берлине"
        date = "1936-08-01T00:00:00"
        end_date = "1936-08-16T00:00:00"
        description = "Летние Олимпийские игры, проходившие в нацистской Германии"
        location = "Берлин, Германия"
        importance = 4
        category_id = $categoryLookup["Спорт"]
    },
    @{
        title = "Создание Европейского Союза"
        date = "1993-11-01T00:00:00"
        description = "Образование Европейского Союза после подписания Маастрихтского договора"
        location = "Европа"
        importance = 5
        category_id = $categoryLookup["Политика"]
    },
    @{
        title = "Изобретение World Wide Web"
        date = "1989-03-12T00:00:00"
        description = "Тим Бернерс-Ли представил предложение о создании World Wide Web"
        location = "ЦЕРН, Швейцария"
        importance = 5
        category_id = $categoryLookup["Технологии"]
    },
    @{
        title = "Запуск первого iPhone"
        date = "2007-06-29T00:00:00"
        description = "Запуск первого iPhone, ознаменовавший революцию в мобильных технологиях"
        location = "США"
        importance = 4
        category_id = $categoryLookup["Технологии"]
    },
    @{
        title = "Реформация"
        date = "1517-10-31T00:00:00"
        end_date = "1648-10-24T00:00:00"
        description = "Религиозное движение в Западной Европе, направленное на реформирование церкви"
        location = "Европа"
        importance = 5
        category_id = $categoryLookup["Религия"]
    },
    @{
        title = "Путешествие Христофора Колумба"
        date = "1492-08-03T00:00:00"
        end_date = "1493-03-15T00:00:00"
        description = "Первое путешествие Колумба в Америку"
        location = "Атлантический океан"
        importance = 5
        category_id = $categoryLookup["Исследования"]
    },
    @{
        title = "Полет на Луну"
        date = "1969-07-20T00:00:00"
        description = "Первая высадка человека на Луну в рамках миссии Аполлон-11"
        location = "Луна"
        importance = 5
        category_id = $categoryLookup["Исследования"]
    },
    @{
        title = "Строительство Колизея"
        date = "0072-01-01T00:00:00"
        end_date = "0080-01-01T00:00:00"
        description = "Строительство знаменитого римского амфитеатра"
        location = "Рим, Италия"
        importance = 4
        category_id = $categoryLookup["Архитектура"]
    },
    @{
        title = "Первый чемпионат мира по футболу"
        date = "1930-07-13T00:00:00"
        end_date = "1930-07-30T00:00:00"
        description = "Первый международный турнир по футболу среди сборных команд"
        location = "Уругвай"
        importance = 3
        category_id = $categoryLookup["Спорт"]
    },
    @{
        title = "Изобретение парового двигателя"
        date = "1712-01-01T00:00:00"
        description = "Изобретение Томасом Ньюкоменом первого практического парового двигателя"
        location = "Англия"
        importance = 5
        category_id = $categoryLookup["Технологии"]
    },
    @{
        title = "Второй Ватиканский собор"
        date = "1962-10-11T00:00:00"
        end_date = "1965-12-08T00:00:00"
        description = "Важный собор католической церкви, внесший значительные изменения в литургию и отношения с другими конфессиями"
        location = "Ватикан"
        importance = 4
        category_id = $categoryLookup["Религия"]
    },
    @{
        title = "Экспедиция Магеллана"
        date = "1519-09-20T00:00:00"
        end_date = "1522-09-06T00:00:00"
        description = "Первое кругосветное путешествие, начатое под руководством Фернана Магеллана"
        location = "Мировой океан"
        importance = 5
        category_id = $categoryLookup["Исследования"]
    },
    @{
        title = "Чернобыльская катастрофа"
        date = "1986-04-26T00:00:00"
        description = "Крупнейшая в истории атомной энергетики авария"
        location = "Чернобыль, УССР"
        importance = 5
        category_id = $categoryLookup["Наука"]
    },
    @{
        title = "Строительство Великой Китайской стены"
        date = "0220-01-01T00:00:00"
        end_date = "1644-01-01T00:00:00"
        description = "Строительство одного из крупнейших архитектурных сооружений в истории"
        location = "Китай"
        importance = 5
        category_id = $categoryLookup["Архитектура"]
    },
    @{
        title = "Первые современные Олимпийские игры"
        date = "1896-04-06T00:00:00"
        end_date = "1896-04-15T00:00:00"
        description = "Возрождение Олимпийских игр в современном формате"
        location = "Афины, Греция"
        importance = 4
        category_id = $categoryLookup["Спорт"]
    },
    @{
        title = "Изобретение микропроцессора"
        date = "1971-11-15T00:00:00"
        description = "Создание Intel 4004, первого коммерчески доступного микропроцессора"
        location = "США"
        importance = 5
        category_id = $categoryLookup["Технологии"]
    }
)

Write-Host "Добавление новых событий..."
$eventIdMap = @{}
foreach ($event in $events) {
    try {
        $response = Invoke-RestMethod -Uri "$apiBaseUrl/events" -Method Post -Body ($event | ConvertTo-Json) -ContentType "application/json"
        Write-Host "Событие добавлено: $($response.title), ID: $($response.id)"
        $eventIdMap[$response.title] = $response.id
    }
    catch {
        Write-Host "Ошибка при добавлении события $($event.title): $_"
    }
}

# Получаем все события для определения их ID
$allEvents = Invoke-RestMethod -Uri "$apiBaseUrl/events" -Method Get
foreach ($event in $allEvents) {
    if (-not $eventIdMap.ContainsKey($event.title)) {
        $eventIdMap[$event.title] = $event.id
    }
}

# Добавление новых связей между событиями
$connections = @(
    @{
        cause_id = $eventIdMap["Строительство Берлинской стены"]
        effect_id = $eventIdMap["Падение Берлинской стены"]
        description = "Строительство стены привело к последующему падению"
        strength = 3
    },
    @{
        cause_id = $eventIdMap["Строительство Берлинской стены"]
        effect_id = $eventIdMap["Холодная война"]
        description = "Берлинская стена как символ Холодной войны"
        strength = 2
    },
    @{
        cause_id = $eventIdMap["Падение Берлинской стены"]
        effect_id = $eventIdMap["Распад СССР"]
        description = "Падение стены способствовало распаду СССР"
        strength = 2
    },
    @{
        cause_id = $eventIdMap["Холодная война"]
        effect_id = $eventIdMap["Полет на Луну"]
        description = "Космическая гонка как результат Холодной войны"
        strength = 3
    },
    @{
        cause_id = $eventIdMap["Создание Европейского Союза"]
        effect_id = $eventIdMap["Распад СССР"]
        description = "Распад СССР способствовал созданию ЕС"
        strength = 1
    },
    @{
        cause_id = $eventIdMap["Изобретение World Wide Web"]
        effect_id = $eventIdMap["Запуск первого iPhone"]
        description = "Развитие веб-технологий привело к созданию смартфонов"
        strength = 2
    },
    @{
        cause_id = $eventIdMap["Путешествие Христофора Колумба"]
        effect_id = $eventIdMap["Экспедиция Магеллана"]
        description = "Открытия Колумба вдохновили другие экспедиции"
        strength = 2
    },
    @{
        cause_id = $eventIdMap["Изобретение парового двигателя"]
        effect_id = $eventIdMap["Изобретение World Wide Web"]
        description = "Промышленная революция привела к информационной революции"
        strength = 1
    }
)

Write-Host "Добавление новых связей..."
foreach ($connection in $connections) {
    try {
        if ($connection.cause_id -and $connection.effect_id) {
            $response = Invoke-RestMethod -Uri "$apiBaseUrl/connections" -Method Post -Body ($connection | ConvertTo-Json) -ContentType "application/json"
            Write-Host "Связь добавлена: ID: $($response.id), От: $($connection.cause_id) К: $($connection.effect_id)"
        }
        else {
            Write-Host "Пропуск связи из-за отсутствия ID событий: $($connection | ConvertTo-Json)"
        }
    }
    catch {
        Write-Host "Ошибка при добавлении связи: $_"
        Write-Host "Данные связи: $($connection | ConvertTo-Json)"
    }
}

Write-Host "Добавление тестовых данных завершено!" 