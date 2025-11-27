// ------------------------------------
// Настройки тайлов и карты
// ------------------------------------

// Размер тайла в пикселях (каждый "пиксель" карты)
const tileSize = 16;

// Массив доступных тайлов. Каждый тайл имеет id и цвет в HEX
const tiles = [
    {id:0, color:'#ffffff'}, // пустой белый
    {id:1, color:'#00ff00'}, // зелёная трава
    {id:2, color:'#8B4513'}, // коричневая земля
    {id:3, color:'#0000ff'}, // синий вода
    {id:4, color:'#808080'}  // серый камень
];

// Тайл, который выбран для рисования (по умолчанию трава)
let selectedTile = 1;

// Ширина и высота карты в тайлах
const mapWidth = 100;
const mapHeight = 60;

// -----------------------------
// ПАЛИТРА ТАЙЛОВ
// -----------------------------

// Получаем HTML-контейнер для палитры
const paletteDiv = document.getElementById('palette');

// Для каждого тайла создаём квадрат в палитре
tiles.forEach(tile => {

    // Создаём div для тайла
    const div = document.createElement('div');

    // Добавляем CSS класс .tile
    div.classList.add('tile');

    // Задаём цвет фона div
    div.style.background = tile.color;

    // Обработчик клика по тайлу
    div.addEventListener('click', () => {

        // Запоминаем выбранный тайл
        selectedTile = tile.id;

        // Снимаем выделение со всех тайлов
        document.querySelectorAll('.tile').forEach(t => t.classList.remove('selected'));

        // Выделяем текущий тайл
        div.classList.add('selected');
    });

    // Если это выбранный тайл по умолчанию — выделяем
    if(tile.id === selectedTile) div.classList.add('selected');

    // Добавляем тайл в палитру
    paletteDiv.appendChild(div);
});

// ------------------------------------
// Phaser 3 конфигурация
// ------------------------------------
const config = {
    type: Phaser.AUTO,                  // Phaser выбирает WebGL или Canvas автоматически
    width: mapWidth * tileSize,         // ширина canvas в пикселях
    height: mapHeight * tileSize,       // высота canvas
    backgroundColor: '#ffffff',         // цвет фона сцены
    scene: {                            // сцена Phaser
        preload: preload,               // функция загрузки ресурсов
        create: create,                 // функция создания сцены
        update: update                  // функция обновления сцены каждый кадр
    }
};

// Создаём Phaser Game
const game = new Phaser.Game(config);

// Переменная для графики (рисование тайлов)
let graphics;

// 2D массив карты (каждая ячейка хранит id тайла)
let mapMatrix = [];

// ------------------------------------
// Функции для карты
// ------------------------------------

// Создаёт пустую карту width x height (все тайлы 0)
function createEmptyMap(width, height){
    return Array.from({length: height}, ()=>Array(width).fill(0));
}

// Генерация примерной карты с границами, землёй и водой
function createExampleMap(width, height){
    return Array.from({length: height}, (_, y) =>
        Array.from({length: width}, (_, x) => {
            if(y===0 || y===height-1 || x===0 || x===width-1) return 4;   // каменные границы
            if(y>20 && y<25 && x>30 && x<70) return 2;                     // земля в центре
            if((x+y)%10===0) return 3;                                     // случайные водяные тайлы
            return 1;                                                      // остальная трава
        })
    );
}

// ------------------------------------
// Phaser сцена
// ------------------------------------
function preload(){
    // Здесь можно загружать картинки/спрайты, пока пусто
}

function create(){
    // Создаём объект для рисования
    graphics = this.add.graphics();

    // Создаём стартовую карту
    mapMatrix = createExampleMap(mapWidth, mapHeight);

    // Отрисовываем карту на экране
    drawMap();

    // Обработчики мыши для рисования
    this.input.on('pointerdown', pointer => {
        drawTile(pointer);                 // рисуем по клику
        this.input.on('pointermove', drawTile); // рисуем при перемещении мыши
    });

    this.input.on('pointerup', () => {
        this.input.off('pointermove', drawTile); // останавливаем рисование
    });
}

function update(){
    // Можно обновлять анимацию, пока оставляем пустым
}

// ------------------------------------
// Рисуем карту
// ------------------------------------
function drawMap(){
    graphics.clear(); // очищаем canvas перед рисованием

    for(let y=0; y<mapHeight; y++){
        for(let x=0; x<mapWidth; x++){
            // Получаем id тайла
            const tileId = mapMatrix[y][x];

            // Получаем цвет тайла
            const color = Phaser.Display.Color.HexStringToColor(tiles[tileId].color).color;

            // Задаём цвет для заливки
            graphics.fillStyle(color, 1);

            // Рисуем прямоугольник тайла
            graphics.fillRect(x*tileSize, y*tileSize, tileSize, tileSize);

            // Добавляем сетку для видимости тайлов
            graphics.lineStyle(1, 0x000000, 0.2);
            graphics.strokeRect(x*tileSize, y*tileSize, tileSize, tileSize);
        }
    }
}

// ------------------------------------
// Рисуем тайл по клику мыши
// ------------------------------------
function drawTile(pointer){
    // Вычисляем координаты тайла в массиве
    const x = Math.floor(pointer.x / tileSize);
    const y = Math.floor(pointer.y / tileSize);

    // Проверяем границы карты
    if(x>=0 && x<mapWidth && y>=0 && y<mapHeight){
        // Обновляем матрицу карты
        mapMatrix[y][x] = selectedTile;

        // Перерисовываем карту
        drawMap();
    }
}

// ------------------------------------
// Получить копию текущей матрицы карты
// ------------------------------------
function getMap(){
    return mapMatrix.map(row => [...row]);
}

// ------------------------------------
// Сохранение карты через API
// ------------------------------------
document.getElementById('saveBtn').addEventListener('click', async () => {
    // Получаем текущую карту как 2D массив
    const matrix = getMap();

    // Спрашиваем у пользователя название карты
    const mapName = prompt("Введите название карты:");

    // Если пользователь не ввёл название — прекращаем сохранение
    if(!mapName){
        alert("Название обязательно!");
        return;
    }

    try {
        // Отправляем POST-запрос на backend (FastAPI)
        const response = await fetch("http://localhost:8000/map/add_map/", {
            method: "POST",

            // Заголовки запроса
            headers:{
                "Content-Type":"application/json",  // мы отправляем JSON
                "Authorization":"Bearer " + localStorage.getItem("token") // если используем JWT
            },

            // Тело запроса — JSON объект с именем карты и матрицей
            body: JSON.stringify({ map_name: mapName, matrix: matrix })
        });

        // Если сервер вернул ошибку (status >=400)
        if(!response.ok) throw new Error("Ошибка сохранения");

        // Всё прошло успешно — уведомляем пользователя
        alert("Карта сохранена!");
    } catch(e){
        // Если произошла ошибка при запросе — выводим в консоль и показываем alert
        console.error(e);
        alert("Не удалось сохранить карту");
    }
});

