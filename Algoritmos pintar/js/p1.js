//Declaro variables
var x = 0;
var y = 0;
var x2 = 0;
var y2 = 0;
var steps = 0;
var points = [[]];
var buffer = [[]];
var algoritmo = 0;
var canvas;
var ctx;

window.onload = function() { //espera a cargar el html y no busca funciones que no existen para no referirse a esas clases
	this.canvas = document.getElementById("canvas");
	this.ctx = document.getElementById("canvas").getContext("2d");
	changeAxis();
	points.shift();
	buffer.shift();
	click();
};

function changeAxis() {
	canvas = document.getElementById("canvas");
	ctx = canvas.getContext("2d");
	ctx.translate(300, 300); // Centramos los ejes
	pintaEjes(ctx, "white", "black");
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

	if (i % 2 == 0) {
		//No vuelve a pintar las lineas porque evalua que la longitud sea modulo de dos
		switch (algoritmo) {
			case 0:
				drawLineSlope(
					this.points[i - 2][0],
					this.points[i - 2][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
					this.points[i - 1][0],
					this.points[i - 1][1]
				);
				break;
			case 1:
				drawLineDDA(
					this.points[i - 2][0],
					this.points[i - 2][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
					this.points[i - 1][0],
					this.points[i - 1][1]
				);
				break;
			case 2:
				drawLineBerserham(
					this.points[i - 2][0],
					this.points[i - 2][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
					this.points[i - 1][0],
					this.points[i - 1][1]
				);
				break;
			case 3:
				drawLineSlopeMal(
					this.points[i - 2][0],
					this.points[i - 2][1], // Como la i es la longitud, pintamos los dos ultimos puntos (i-1 e i-2)
					this.points[i - 1][0],
					this.points[i - 1][1]
				);
				break;
		}
	}
}

function click() {
	//Añadimos un addEventListener al canvas, para reconocer el click
	canvas.addEventListener(
		"click",
		function(e) {
			points.push([e.clientX - 675, e.clientY - 330]); //Hacemos el push de las coord
			let node = document.createElement("P"); // Create a <li> node
			let textnode = document.createTextNode([
				e.clientX - 675,
				e.clientY - 330
			]); // Para mostrar los puntos
			node.appendChild(textnode);
			document.getElementById("puntos").appendChild(node);
			paint(e.clientX - 675, e.clientY - 330, points.length); //Pintamos y pasamos como parametro la longitud
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

function drawLineSlopeMal(x1, y1, x2, y2) {
	let x = x1;
	let y = y1;
	let incx = 1;
	let m = (y2 - y1) / (x2 - x1);
	let b = y1 - m * x1;

	while(x <= x2) {
		x += incx;
		y = Math.round(m * x + b);
		console.log(x, y);
		drawPoint(x, y);
	}
}

function drawLineSlope(x1, y1, x2, y2) {
	let m = (y2 - y1) / (x2 - x1);
	let incx = 1;
	let incy = 1;
	let b = y1 - m * x1;

	if (x2 - x1 < 0) incx = -1; //Si vamos de > a <
	if (y2 - y1 < 0) incy = -1; // Si vamos de  > a <

	//si x2 y x1 son iguales m va a ser infinito entonces solo incremento el valor de y
	if (m == Infinity || m == -Infinity) {
		while (y1 - y2 != 0) {
			y1 += incy;
			console.log(x1, y1);
			drawPoint(x1, y1);
		}
	} else {
		//Para pendientes grandes invierto el proceso asi los pixeles no quedan muy separados si la distancia 
		//en x es pequeña y en y grande
		if (Math.abs(x2 - x1) < Math.abs(y2 - y1)) {
			while (y1 - y2 != 0) {
				if (y1 - y2 == 0) return;
				y1 += incy;
				x1 = Math.round((y1 - b) / m);
				console.log(x1, y1);
				drawPoint(x1, y1);
			}
		} else {
			while (x1 - x2 != 0) {
				if (x1 - x2 == 0) return;
				x1 += incx;
				y1 = Math.round(m * x1 + b);
				console.log(x1, y1);
				drawPoint(x1, y1);
			}
		}
	}
}

function drawLineDDA(x1, y1, x2, y2) {
	let dx = x2 - x1;
	let dy = y2 - y1;
	let x = x1;
	let y = y1;
	let l;

	if(Math.abs(dx)>Math.abs(dy)){
		l = Math.abs(dx);
	}else{
		l = Math.abs(dy);
	}

	//incrementos en x e y
	let ax = dx / l;
	let ay = dy / l;

	let i = 0;
	while (i <= l) {
		console.log(Math.floor(x), Math.floor(y));
		drawPoint(Math.floor(x), Math.floor(y));
		x += ax;
		y += ay;
		i++;
	}
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
		console.log(xB, yB);
		drawPoint(xB, yB);
	}
}

function aplicaSlope() {
	limpiaPuntos();
	algoritmo = 0;
	pintaEjes(ctx, "brown", "#B1F3CB");
}

function aplicaDDA() {
	limpiaPuntos();
	algoritmo = 1;
	pintaEjes(ctx, "orange", "#B1F3CB");
}

function aplicaBerserham() {
	limpiaPuntos();
	algoritmo = 2;
	pintaEjes(ctx, "green", "#B1F3CB");
}

function aplicaSlopeMal() {
	limpiaPuntos();
	algoritmo = 3;
	pintaEjes(ctx, "red", "#B1F3CB");
}

function limpiaPuntos(){
        var e = document.getElementById("puntos");
        
        //voy borrando cada elemento
        var child = e.lastElementChild;  
        while (child) { 
            e.removeChild(child); 
            child = e.lastElementChild; 
        }
}

