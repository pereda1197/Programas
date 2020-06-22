//Declaro variables
var points = [[]];
var buffer = [[]];
var funciones = [[]];
var node = document.createElement("P"); // Create a <li> node
var textnode = [];
var canvas;
var ctx;

var x0,y0 = 1;

window.onload = function () { //espera a cargar el html y no busca funciones que no existen para no referirse a esas clases
    this.canvas = document.getElementById("canvas");
    this.ctx = document.getElementById("canvas").getContext("2d");
    changeAxis();
    points.shift();
    buffer.shift();
    funciones.shift();
    textnode.shift();
};

function changeAxis() {
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    ctx.translate(300, 300); // Centramos los ejes
    pintaCanvas(ctx, "green");
}

function pintaCanvas(ctx,colorCanvas) {
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-10000, -100);
    ctx.fillStyle = colorCanvas; //Color del canvas
    ctx.fillRect(-600, -600, 1400, 1400);
    ctx.fill();
    ctx.closePath();
    ctx.beginPath();
}

function pinta() {
    let a = parseFloat($('.a').val());
    let b = parseFloat($('.b').val());
    let c = parseFloat($('.c').val());
    let d = parseFloat($('.d').val());
    let e = parseFloat($('.e').val());
    let f = parseFloat($('.f').val());
    let n = parseFloat($('.T').val());
    spierpinsky(a,b,c,d,e,f,n);
}

function limpia() {
    points = [[]];
    buffer = [[]];
    funciones = [[]];
    textnode = [];
    x0,y0 = 1;
    node = document.createElement("P"); // Create a <li> node
    pintaCanvas(ctx, "green");

    var e = document.getElementById("funciones");

    //voy borrando cada elemento
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
}

function anadeFuncion(){
    let a = parseFloat($('.a').val());
    let b = parseFloat($('.b').val());
    let c = parseFloat($('.c').val());
    let d = parseFloat($('.d').val());
    let e = parseFloat($('.e').val());
    let f = parseFloat($('.f').val());

    let i = funciones.length;
    textnode[i] = document.createTextNode("Función "+i+": ("+[
        a,b,c,d,e,f
    ]+")  "); // Para mostrar las funciones
    node.appendChild(textnode[i]);
    document.getElementById("funciones").appendChild(node);

    console.log(i);
    /* console.log(a);
    console.log(b); */

    funciones.push([a,b,c,d,e,f]);
    console.log(funciones);
}

function borraFuncion(){
    let n = funciones.length;
    let num = parseInt($('.funcion1').val());

    if (num>=n){
        return console.error("No hay tantas funciones");
    }

    funciones.splice(num,1);
    
    //bucle para cuando borro una función que el número del resto baje un número
    for (var i = 0; i < n; i++){
        node.removeChild(textnode[i]); //borro todas para actualizar el número de la función
        textnode[i] = document.createTextNode("Función "+i+": ("+funciones[i]+")  "); // Para mostrar las funciones
        node.appendChild(textnode[i]);
    }
    node.removeChild(textnode[n-1]); //borro la ultima porque con el bucle se añade una de más
    
    console.log(funciones);
}

function modificaFuncion(){
    let n = funciones.length;
    let num = parseInt($('.funcion2').val());
    let a = parseFloat($('.a').val());
    let b = parseFloat($('.b').val());
    let c = parseFloat($('.c').val());
    let d = parseFloat($('.d').val());
    let e = parseFloat($('.e').val());
    let f = parseFloat($('.f').val());

    if (num>=n){
        return console.error("No hay tantas funciones");
    }

    funciones.splice(num,1);
    funciones.push([a,b,c,d,e,f]);

    //bucle para cuando borro una función que el número del resto baje un número
    for (var i = 0; i < n; i++){
        node.removeChild(textnode[i]); //borro todas para actualizar el número de la función
        textnode[i] = document.createTextNode("Función "+i+": ("+funciones[i]+")  "); // Para mostrar las funciones
        node.appendChild(textnode[i]);
    }
}

function background(){
    pintaCanvas(ctx,$('.background').val());
}

function spierpinsky(a,b,c,d,e,f,n){
    canvas = document.getElementById("canvas");
	ctx = canvas.getContext("2d");
	let Ax, Ay, Bx, By, Cx, Cy;
    let color = $('.color').val();

	if (!n) {
		ctx.beginPath()
		ctx.moveTo(a, b);
		ctx.lineTo(c, d);
		ctx.lineTo(e, f);
		ctx.lineTo(a, b);
		ctx.strokeStyle = color;
		ctx.stroke();
		ctx.closePath();
	} else {
		Ax = a + (c - a) / 2;
		Ay = b + (d - b) / 2;
		Bx = e + (c - e) / 2;
		By = f + (d - f) / 2;
		Cx = a + (e - a) / 2;
		Cy = b + (f - b) / 2;
		spierpinsky(Ax, Ay, c, d, Bx, By, n - 1);
		spierpinsky(a, b, Ax, Ay, Cx, Cy, n - 1);
		spierpinsky(Cx, Cy, Bx, By, e, f, n - 1);
	}
}

function mandelbrot() {
	canvas = document.getElementById("canvas");
	ctx = canvas.getContext("2d");
	var magnificationFactor = 200;
	var panX = 0;
    var panY = 0;
    let color = $('.color').val();

	for (var x = -500; x < canvas.width; x++) {
		for (var y = -400; y < canvas.height; y++) {
			var belongsToSet =
				validoParaMandelbrot(x / magnificationFactor - panX,
					y / magnificationFactor - panY);
			if (belongsToSet) {
				ctx.fillStyle = color;
				ctx.fillRect(x, y, 1, 1); //dibuja pixel
			}
		}
	}
}

function validoParaMandelbrot(x, y) {
	var realComponentOfResult = x;
	var imaginaryComponentOfResult = y;
	for (var i = 0; i < 180; i++) {
		// Calcula las componentes real e imaginaria
		var tempRealComponent = realComponentOfResult * realComponentOfResult - imaginaryComponentOfResult * imaginaryComponentOfResult + x;
		var tempImaginaryComponent = 2 * realComponentOfResult * imaginaryComponentOfResult + y;
		realComponentOfResult = tempRealComponent;
		imaginaryComponentOfResult = tempImaginaryComponent;
	}
	if (realComponentOfResult * imaginaryComponentOfResult < 5)
		return true; // Valido para mandelbrot
	return false; //No valido para mandelbrot
}

function koch(){
    pintaCanvas(ctx,"white");
    fractal([-200,-150], [200,-150], 5);
    fractal([0,200], [-200,-150], 5);
    fractal([200,-150], [0,200], 5);
}

function tree(){
    DrawLineTree([0,300],[0,100]);    
    tree_fractal([0,100],[0,300],75, 10);
}

function tree_fractal(A, B, len, depth){

    if (depth <= 0){
        return null;
    }
     
    var E = add(multiply(divide(minus(A, B), length(A, B)), len), A);

    var V1 = divide(minus(E,A), length(E,A));
    var V2 = [V1[1], -V1[0]];        
    var C = add(multiply(V2, len/2), E);
    
    var V3 = [-V1[1], V1[0]];
    var D = add(multiply(V3, len/2), E);
       
    C[0] = C[0] + (Math.random()-0.5) * length(B,A) * .3;
    C[1] = C[1] + (Math.random()-0.5) * length(B,A) * .1;
    D[0] = D[0] + (Math.random()-0.5) * length(B,A) * .05;
    D[1] = D[1] + (Math.random()-0.5) * length(B,A) * .1;

    DrawLineTree(A,D);
    DrawLineTree(A,C);
    
    tree_fractal(C,A,len/1.3,depth-1);
    tree_fractal(D,A,len/1.3,depth-1);

};

function fractal(A, B, depth){
    
    if (depth < 0){
        return null;
    }

    var C = divide(add(multiply(A, 2), B), 3);
    var D = divide(add(multiply(B, 2), A), 3);
    var F = divide(add(A, B), 2);
    
    var V1 = divide(minus(F, A), length(F, A));
    var V2 = [V1[1], -V1[0]];

    var E = add(multiply(V2, Math.sqrt(3)/6 * length(B, A)), F);

    DrawLineKoch(A, B, "black");

    if (depth !=0){
        for (var i=0;i<10;i++)
            DrawLineKoch(C, D, "white");
    };
    
    fractal(A, C, depth-1);
    fractal(C, E, depth-1);
    fractal(E, D, depth-1);
    fractal(D, B, depth-1);

};

function multiply(v, num){
    return [v[0]*num, v[1]*num];
};

function divide(v, num){
    return [v[0]/num, v[1]/num];
};
 
function add(a, b){
    return [a[0]+b[0], a[1]+b[1]];
};

function minus(a, b){
    return [a[0]-b[0], a[1]-b[1]];
};

function length(a, b){
    return Math.sqrt(Math.pow(a[0] - b[0],2) + 
                     Math.pow(a[1] - b[1],2));
};

function DrawLineKoch(a, b, c){
    ctx.beginPath();
    ctx.strokeStyle = c;
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
    ctx.closePath();
};

function DrawLineTree(a, b){
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
    ctx.closePath();
};