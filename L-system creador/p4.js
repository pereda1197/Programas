//L-SYSTEM

var Turtle = function( x, y, angulo ){
    this.x = x || 0;
    this.y = y || 0;
    this.angulo = angulo || 0;
};
Turtle.prototype = {
    clone : function(){
        return new Turtle( this.x, this.y, this.angulo );
    }
};

var Lsystem = function(axioma, regla, longitud, angulo ) {

    this.axioma = axioma || "f+f";
    this.regla = regla || "f++f";
    this.produccion = "";

    this.longitud = longitud || 10;
    this.angulo = angulo || 0;

};

Lsystem.prototype = {

    moveTurtle:function( ctx, char, turtle ){

        //mueve adelante
        if (char == 'f'){
            turtle.x += Math.cos( turtle.angulo ) * this.longitud;
            turtle.y += Math.sin( turtle.angulo ) * this.longitud;
            ctx.lineTo( turtle.x, turtle.y );
        }

        //rota derecha
        if (char == '+'){
            turtle.angulo += this.angulo;
        }

        //rota izquierda
        if (char == '-'){
            turtle.angulo -= this.angulo;
        }

    },

    render : function( ctx ){

        var turtle = new Turtle(0,0);
        var tmp = new Turtle();

        ctx.save();
        ctx.translate( ctx.canvas.width / 2, ctx.canvas.height / 2 );
        ctx.beginPath();
        ctx.moveTo( turtle.x, turtle.y );

        for ( var i = 1; i < this.produccion.length; i++){

            var char = this.produccion.charAt( i ).toLowerCase();


            //Escanea una rama
            if ( char == '[' ){

                if ( this.produccion.substr( i+1, this.produccion.length ).lastIndexOf( ']' ) == -1 ) continue;
                ctx.stroke();

                tmp = turtle.clone();
                ctx.save();
                ctx.beginPath();
                ctx.moveTo( tmp.x, tmp.y, 2, 0, Math.PI * 2 );

                while ( char != ']'){
                    char = this.produccion.charAt( i++ );
                    this.moveTurtle( ctx, char, tmp );
                }
                ctx.stroke();
                ctx.restore();

                ctx.beginPath();
                ctx.arc( turtle.x, turtle.y, 2, 0, Math.PI * 2 );
                ctx.moveTo( turtle.x, turtle.y );

            }else{

                this.moveTurtle( ctx, char, turtle );
            }
        }
        ctx.stroke();
        ctx.restore();
    },

    compute : function( gens ){

        this.produccion = this.axioma.toLowerCase();
        var prod = '';
        var generacion = 0;
        while ( generacion < gens ){

            for ( var i = 0; i < this.produccion.length; i++ ){

                if( this.produccion.charAt( i ) == 'f' ){
                    prod += this.regla;
                }else{
                    prod += this.produccion.charAt( i );
                }
            }
            this.produccion = prod;
            generacion++;
        }
    }
};

// MAIN
var canvas;
var ctx;
var system;
var parametros;

window.onload = function() { //espera a cargar el html y no busca funciones que no existen para no referirse a esas clases
	this.canvas = document.getElementById("canvas");
    this.ctx = document.getElementById("canvas").getContext("2d");
    this.system = new Lsystem();
    this.parametros = document.getElementById( "parametros" );
    parametros.addEventListener( "keyup", updateSettings );
    parametros.addEventListener( "mouseup", updateSettings );
    updateSettings();
};

var w = 1000;
var h = 1000;

function updateSettings(){


    system.longitud   = document.getElementById( "longitud" ).value;
    system.angulo    = document.getElementById( "angulo" ).value * ( Math.PI / 180 );
    system.axioma    = document.getElementById( "axioma" ).value;
    system.regla     = document.getElementById( "regla" ).value;
    system.produccion = "";

    ctx.clearRect( 0, 0, w,h );

    var generacion = document.getElementById( "generacion" ).value;
    system.compute( generacion );
    system.render( ctx );
    document.getElementById( "produccion" ).value = system.produccion;

}

window.addEventListener("mensaje", receiveMessage, false);
function receiveMessage(event){
    if( event.data == "inicio" ){
        updateSettings();
    }
    if( event.data == "stop" ){
        ctx.clearRect( 0, 0, w,h );
    }
}
