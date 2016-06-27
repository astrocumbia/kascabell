<!DOCTYPE html>
<html lang="es">
    <head>
        <title>Amenizador</title>

        <link href="public/css/bootstrap.min.css" rel="stylesheet" type="text/css">
        <link href="public/css/mystyle.css" rel="stylesheet" type="text/css">
        <script src="public/js/jquery.min.js"></script>
        <script src="public/js/simple-slider.js"></script>
        <link href="public/css/simple-slider.css" rel="stylesheet" type="text/css" />
    </head>
    <body>
        <div class="container">
            <div class="content" style="color:white;">

                <div class="row" style="padding-bottom:20px; font-size:15px;">
                  <div class="col-md-8 col-md-offset-2">
                    <span class="glyphicon glyphicon-phone"></span>
                    <span id="arduino" style="color: #00d5ff;">0</span>
                  </div>
                </div>

                <div class="row" style="padding-bottom:10px;">
                  <div class="col-md-8  col-md-offset-2 text-center">
                    <img id="imgcover" src="store/imgs/default.jpg"  class="img-circle">
                  </div>
                </div>

                <div class="row" style="padding-bottom:10px;">
                  <div class="col-md-12 text-center" id="songtitle">
                    El taxi - keneddi- Go Joe
                  </div>
                </div>

                <!-- CONTROLLERS -->
                <div class="row">
                  <div class="col-md-12 text-center">

                    <!-- STOP BUTTON -->
                    <button type="button" class="btn  btn-sm btn-round" onclick="stopBtn();">
                      <span class="glyphicon glyphicon-stop"></span>
                    </button>

                    <!-- BACKWARD BUTTON -->
                    <button type="button" class="btn btn-sm btn-round" onclick="backwardBtn();">
                      <span class="glyphicon glyphicon-fast-backward"></span>
                    </button>

                    <!-- PLAY BUTTON -->
                    <button type="button" class="btn btn-lg btn-round" onclick="playBtn();" id="playbtn">
                      <span class="glyphicon glyphicon-play"></span>
                    </button>

                    <!-- PLAY PAUSE -->
                    <button type="button" class="btn btn-lg btn-round hidden" onclick="pauseBtn();" id="pausebtn">
                      <span class="glyphicon glyphicon-pause"></span>
                    </button>

                    <!-- FORWARD BUTTON -->
                    <button type="button" class="btn btn-sm btn-round" onclick="forwardBtn();">
                      <span class="glyphicon glyphicon-fast-forward"></span>
                    </button>

                    <button type="button" class="btn btn-sm btn-round" onclick="repeatBtn();">
                      <span class="glyphicon glyphicon-repeat"></span>
                    </button>

                  </div>
                </div>
                <!-- /CONTROLLERS -->

                <!-- VOLUME CONTROLLER -->
                <div class="row" style="padding-top:10px;">
                  <div class="col-md-1">
                    <span class="glyphicon glyphicon-volume-up"></span>
                  </div>
                  <div class="col-md-10 text-center">
                    <input id="sliderVol" type="range" min="0" max="150" step="10" onchange="setVolume(this.value)"/>
                  </div>
                </div>

            </div>
        </div>

        <script>
          function setVolume(value){
            $.post( "/music/volume", { volume: ""+value } );
          }

					 setInterval(function(){
            $.get("/arduino", function(data){
              $('#arduino').text( data.sensor );
              /*
              if( data.sensor < 600){
                setVolume(40)
              }
              else {
                setVolume(150)
              }*/
              //setVolume(data.sensor/10);
            });

						 $.get( "/music/status", function( data ) {
								$('#songtitle').text(data.title);
                $('#imgcover').attr("src", data.img)
                $('#sliderVol').val(data.volume)

                if( data.active ){
                  	console.log("MUSIC: PLAY");
     								$('#pausebtn').removeClass( "hidden" )
     								$('#playbtn').addClass("hidden");

                }
                else{
                  	$('#playbtn').removeClass( "hidden" )
     								$('#pausebtn').addClass("hidden");

                }
								console.log(data.title);
 			    		});
					 }, 1500);

           function stopBtn(){
						 $.get( "/music/stop", function( data ) {
								console.log("MUSIC: STOP");
								$('#playbtn').removeClass( "hidden" )
								$('#pausebtn').addClass("hidden");
 			    		});
           }


           function backwardBtn(){
						 $.get( "/music/prev", function( data ) {
								console.log("MUSIC: PREV");
 			    		});
           }


					 function playBtn(){
						 $.get( "/music/play", function( data ) {
								console.log("MUSIC: PLAY");
								$('#pausebtn').removeClass( "hidden" )
								$('#playbtn').addClass("hidden");
 			    		});
           }

           function pauseBtn(){
						 $.get( "/music/pause", function( data ) {
								console.log("MUSIC: PAUSE");
								$('#playbtn').removeClass( "hidden" )
								$('#pausebtn').addClass("hidden");
 			    		});
           }

           function forwardBtn(){
						 $.get( "/music/next", function( data ) {
								console.log("MUSIC: NEXT");
 			    		});
           }

           function repeatBtn(){
             console.log("repeat button")
           }


        </script>
    </body>
</html>
