//Declaro variables
var x = 0;
var y = 0;
var x2 = 0;
var y2 = 0;
var steps = 0;
var points = [[]];
var buffer = [[]];
var canvas;
var ctx;
var startFigure = 0;
var startAnimacion = 0;

var tx, ty, ex, ey, rx, ry, ang;

window.onload = function () { //espera a cargar el html y no busca funciones que no existen para no referirse a esas clases
    this.canvas = document.getElementById("canvas");
    this.ctx = document.getElementById("canvas").getContext("2d");
    changeAxis();
    points.shift();
    buffer.shift();
    /* click(); */
};

function changeAxis() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    ctx.translate(300, 300); // Centramos los ejes
    pintaEjes(ctx, "black", "black");
}

function pintaEjes(ctx, colorEjes, colorCanvas) {
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-10000, -100);
    ctx.fillStyle = colorCanvas; //Color del canvas
    ctx.fillRect(-600, -600, 1400, 1400);
    ctx.fill();
    ctx.closePath();
    ctx.beginPath();
    //eje vertical
    ctx.moveTo(0, -400);
    ctx.lineTo(0, 400);
    ctx.strokeStyle = colorEjes; // Color de los ejes
    ctx.stroke();
    //eje horizontal
    ctx.moveTo(-500, 0);
    ctx.lineTo(500, 0);
    ctx.stroke();
}

function draw(x, y, x2, y2, i) {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "blue"; //Para que se vean los pixeles
    ctx.fillRect(x, y, x2, y2);
    ctx.fill();

    //No vuelve a pintar las lineas porque evalua que la longitud sea modulo de dos
    if (this.startFigure == 0) {
        this.startFigure = 1;
    }
    else {
        this.drawLineBerserham(
            this.points[i - 2][0],
            this.points[i - 2][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
            this.points[i - 1][0],
            this.points[i - 1][1]
        );
    }
}

function click() {
    //Añadimos un addEventListener al canvas, para reconocer el click
    canvas.addEventListener(
        "click",
        function (e) {
            points.push([e.clientX - 567, e.clientY - 317]); //Hacemos el push de las coord
            let node = document.createElement("P"); // Create a <li> node
            let textnode = document.createTextNode([
                e.clientX - 567,
                e.clientY - 317
            ]); // Para mostrar los puntos
            node.appendChild(textnode);
            document.getElementById("puntos").appendChild(node);
            paint(e.clientX - 567, e.clientY - 317, points.length); //Pintamos y pasamos como parametro la longitud
        },
        false
    );
}

function paint(x, y, i) {
    draw(x, y, 5, 5, i);
}

function drawPoint(x, y) {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "blue"; //Para que se vean los pixeles
    ctx.fillRect(x, y, 1, 1);
    ctx.fill();
}

function drawLineBerserham(x1, y1, x2, y2) {
    let xB = x1;
    let yB = y1;
    //funcion abs para tener el valor absoluto
    let dx = Math.abs(x2 - x1);
    let dy = Math.abs(y2 - y1);
    let sx;
    let sy;
    let e;

    //miro para donde incremento (sx)
    if (x2 - x1 > 0) sx = 1;
    else if (x2 - x1 < 0) sx = -1;
    else sx = 0;

    //miro para donde incremento (sy)
    if (y2 - y1 > 0) sy = 1;
    else if (y2 - y1 < 0) sy = -1;
    else sy = 0;

    if (dy > dx) {
        //si dy es mayor que dx los cambio
        let temp = dx;
        dx = dy;
        dy = temp;
        flag = 1; //variable para condiciones
    } else {
        flag = 0;
    }

    //Debe modificarse el error para que el error sea un entero. 
    //sustituimos e por 2 dy - dx 
    e = 2 * dy - dx;
    for (let i = 1; i < dx; i++) {
        while (e > 0) {
            if (flag == 1) xB += sx;
            //si flag 1, incremento a x sx
            else yB += sy;
            //si flag 0, incremento a y sy
            e -= 2 * dx;
        }
        //update x o y
        if (flag == 1) yB += sy;
        else xB += sx;

        //update e (ne)
        e += 2 * dy;
        /* console.log(xB, yB); */
        drawPoint(xB, yB);
    }
}

function trasladar() {
    if (startAnimacion == 0) {
        tx = parseInt($('.transx').val());
        ty = parseInt($('.transy').val());
    }
    let max = this.points.length;
    let matAux = [[1, 0, 0], [0, 1, 0], [tx, ty, 0]];
    let matrix = [];
    for (let i = 0; i < max; i++) {
        this.points[i] = [this.points[i][0], this.points[i][1], 1];
    }
    for (let i = 0; i < max; i++) {
        matrix.push(this.points[i]);
    }
    /* console.log(matrix,matAux); */
    matrix = this.multiply(matrix, matAux);
    this.points.splice(0, this.points.length);
    for (let i = 0; i < max; i++) {
        this.points.push(matrix[i]);
    }
    /* console.log(matrix) */
    this.drawNew();
}

function escalar() {
    if (startAnimacion == 0) {
        ex = parseFloat($('.escx').val());
        ey = parseFloat($('.escy').val());
    }
    let max = this.points.length;
    let matAux = [[ex, 0, 0], [0, ey, 0], [0, 0, 1]];
    let matrix = [];
    for (let i = 0; i < max; i++) {
        this.points[i] = [this.points[i][0], this.points[i][1], 1];
    }
    for (let i = 0; i < max; i++) {
        matrix.push(this.points[i]);
    }
    /* console.log(matrix,matAux); */
    matrix = this.multiply(matrix, matAux);
    this.points.splice(0, this.points.length);
    for (let i = 0; i < max; i++) {
        this.points.push(matrix[i]);
    }
    /* console.log(matrix) */
    this.drawNew();
}

function rotar() {
    if (startAnimacion == 0) {
        ang = (parseFloat($('.ang').val()) * Math.PI) / 180;
        rx = parseFloat($('.rotx').val());
        ry = parseFloat($('.roty').val());
    }
    let max = this.points.length;
    let matAux = [[Math.cos(ang), Math.sin(ang), 0], [-Math.sin(ang), Math.cos(ang), 0], [rx, ry, 1]];
    let matrix = [];
    for (let i = 0; i < max; i++) {
        this.points[i] = [this.points[i][0], this.points[i][1], 1];
    }
    for (let i = 0; i < max; i++) {
        matrix.push(this.points[i]);
    }
    /* console.log(matrix,matAux); */
    matrix = this.multiply(matrix, matAux);
    this.points.splice(0, this.points.length);
    for (let i = 0; i < max; i++) {
        this.points.push(matrix[i]);
    }
    /* console.log(matrix) */
    this.drawNew();
}

function multiply(A, B) {
    let matrizRes = [];
    let vectAux = [0, 0, 0];
    /* console.log(A,B); */
    for (i = 0; i < A.length; i++) {
        for (j = 0; j < 3; j++) {
            for (k = 0; k < 3; k++) {
                vectAux[j] = vectAux[j] + (A[i][k] * B[k][j]);
            }
        }
        /* console.log(vectAux); */
        matrizRes[i] = vectAux;
        vectAux = [0, 0, 0];
    }
    return matrizRes;
}

function drawNew() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    for (let i = 0; i < this.points.length - 1; i++) {
        ctx.fillStyle = "blue"; //Para que se vean los pixeles
        ctx.fillRect(this.points[i][0], this.points[i][1], 5, 5);
        ctx.fill();
        this.drawLineBerserham(
            this.points[i][0],
            this.points[i][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
            this.points[i + 1][0],
            this.points[i + 1][1]
        );
    }
    this.drawLineBerserham(
        this.points[0][0],
        this.points[0][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
        this.points[this.points.length - 1][0],
        this.points[this.points.length - 1][1]
    );
}

function limpia() {
    x = 0;
    y = 0;
    x2 = 0;
    y2 = 0;
    steps = 0;
    points = [[]];
    buffer = [[]];
    startFigure = 0;
    startAnimacion = 0;
    pintaEjes(ctx, "white", "green");
    click();

    var e = document.getElementById("puntos");

    //voy borrando cada elemento
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}

function asignaTrasladar(x, y) {
    tx = x;
    ty = y;
}

function asignaEscalar(x, y) {
    ex = x;
    ey = y;
}

function asignaRotar(x, y, grados) {
    rx = x;
    ry = y;
    ang = grados;
}

function muneco(posicion) {
    if (posicion == 0) { //manos rectas
        pintaEjes(ctx, "white", "white");
        drawLineBerserham(0, 150, 0, 50);
        drawLineBerserham(0, 50, 50, 50);
        drawLineBerserham(0, 50, -50, 0);
        drawLineBerserham(0, 150, -20, 200);
        drawLineBerserham(0, 150, 20, 200);
        drawLineBerserham(0, 50, 0, 0);
        drawLineBerserham(-20, 0, 20, 0);
        drawLineBerserham(-20, 0, -20, -20);
        drawLineBerserham(-20, -20, 20, -20);
        drawLineBerserham(20, 0, 20, -20);
    } else if (posicion == 1) { //mano izquierda arriba
        pintaEjes(ctx, "white", "white");
        drawLineBerserham(0, 150, 0, 50);
        drawLineBerserham(0, 50, 50, 50);
        drawLineBerserham(0, 50, -50, 50);
        drawLineBerserham(0, 150, -20, 200);
        drawLineBerserham(0, 150, 20, 200);
        drawLineBerserham(0, 50, 0, 0);
        drawLineBerserham(-20, 0, 20, 0);
        drawLineBerserham(-20, 0, -20, -20);
        drawLineBerserham(-20, -20, 20, -20);
        drawLineBerserham(20, 0, 20, -20);
    } else { //mano derecha arriba
        pintaEjes(ctx, "white", "white");
        drawLineBerserham(0, 150, 0, 50);
        drawLineBerserham(0, 50, 50, 0);
        drawLineBerserham(0, 50, -50, 50);
        drawLineBerserham(0, 150, -20, 200);
        drawLineBerserham(0, 150, 20, 200);
        drawLineBerserham(0, 50, 0, 0);
        drawLineBerserham(-20, 0, 20, 0);
        drawLineBerserham(-20, 0, -20, -20);
        drawLineBerserham(-20, -20, 20, -20);
        drawLineBerserham(20, 0, 20, -20);
    }

}

function animacion() {
    startAnimacion = 1;
    pintaEjes(ctx, "white", "white");
    let time = 0;
    let antX = 10;
    let antY = 10;
    let sigX = 0;
    let sigY = 0;


    drawLineBerserham(0, 0, antX, antY);
    drawLineBerserham(0, 0, -antX, -antY);
    //introducion
    for (let i = 0; i < 5; i++) {
        time += 1000;

        setTimeout(function () {
            sigX = 2 * antX;
            sigY = -2 * antY;
            drawLineBerserham(antX, antY, sigX, sigY);
            drawLineBerserham(-antX, -antY, -sigX, -sigY);
            console.log(i);
            antX = sigX;
            antY = sigY;

        }, time);


    }

    time += 1000;
    //saludar
    for (let i = 0; i < 5; i++) {
        time += 1000;
        if (i % 2 == 0) {
            setTimeout(function () {
                muneco(0);
            }, time);
        } else {
            setTimeout(function () {
                muneco(1);
            }, time);
        }
    }

    time += 1000;
    //caja mano derecha
    setTimeout(function () {
        muneco(0);
        points = [
            [50, 100],
            [150, 100],
            [150, 0],
            [50, 0],
            [50, 100]
        ];
        asignaTrasladar(0, 0);
        trasladar();
    }, time);



    time += 1000;
    //lanza caja
    for (let i = 0; i < 4; i++) {
        time += 1000;
        setTimeout(function () {
            muneco(2);
            asignaTrasladar(0, -50);
            trasladar();
        }, time);
    }

    time += 1000;
    //rota caja
    for (let i = 0; i < 6; i++) {
        time += 1000;
        setTimeout(function () {
            muneco(2);
            asignaRotar(0, 0, 45);
            rotar();
        }, time);
    }

    time += 1000;
    //recoge caja
    setTimeout(function () {
        muneco(0);
        points = [
            [50, 100],
            [150, 100],
            [150, 0],
            [50, 0],
            [50, 100]
        ];
        asignaTrasladar(0, 0);
        trasladar();
    }, time);

    time += 1000;
    //cambia caja de mano
    setTimeout(function () {
        muneco(0);
        points = [
            [-50, 100],
            [-150, 100],
            [-150, 0],
            [-50, 0],
            [-50, 100]
        ];
        asignaTrasladar(0, 0);
        trasladar();
    }, time);

    time += 1000;
    //escala caja
    setTimeout(function () {
        muneco(2);
        asignaEscalar(2, 2);
        escalar();
    }, time);

    time += 1000;
    //rota caja
    for (let i = 0; i < 3; i++) {
        time += 1000;
        setTimeout(function () {
            muneco(1);
            asignaRotar(0, 0, 45);
            rotar();
        }, time);
    }

    time += 1000;
    //recoge caja
    setTimeout(function () {
        muneco(0);
        points = [
            [50, 100],
            [150, 100],
            [150, 0],
            [50, 0],
            [50, 100]
        ];
        asignaTrasladar(0, 0);
        trasladar();
    }, time);

    time += 1000;
    //saludar
    for (let i = 0; i < 5; i++) {
        time += 1000;
        if (i % 2 == 0) {
            setTimeout(function () {
                muneco(0);
            }, time);
        } else {
            setTimeout(function () {
                muneco(1);
            }, time);
        }
    }
}
