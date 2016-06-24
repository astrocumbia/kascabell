<!DOCTYPE HTML>
<html lang="es">
<head>
	<meta charset="utf-8" />
	<link rel="stylesheet" type="text/css" href="public/bootstrap/css/bootstrap.css" />
	<link rel="stylesheet" type="text/css" href="public/bootstrap/css/style.css" />
  <link rel="stylesheet" type="text/css" href="public/bootstrap/css/mystyle.css" />

  <!-- Include jQuery -->
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
  <!-- Include Simple Slider JavaScript and CSS -->
  <script src="bootstrap/js/simple-slider.js"></script>
  <link href="bootstrap/css/simple-slider.css" rel="stylesheet" type="text/css" />

  <title>Bienvenido</title>
</head>
<body>



	<div id="main" class="row">
    <div class="row">
      <div class="col-md-6 col-md-offset-3 text-center" style="font-size:21px;">

        <div class="row">
          <img id="imgcover" src="imgs/default.jpg"  class="img-circle">
        </div>
				<div class="row" id="title"> Hello - fatboyslim </div>
      </div>
      <div class="col-md-3"></div>

    </div>

    <div class="row text-center" >
      <div class="col-md-6 col-md-offset-3" >
        <a id="BeforeSong" href="#" class="MusicControls"> <span class="glyphicon glyphicon-step-backward" aria-hidden="true"></span></a>
        <a id="PlaySong" href="#" class="MusicControls"> <span class="glyphicon glyphicon-play" aria-hidden="true"></span></a>
				<a id="PauseSong" href="#" class="MusicControls hidden"> <span class="glyphicon glyphicon-pause" aria-hidden="true"></span></a>
				<a id="NextSong" href="#" class="MusicControls"> <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span></a>
      </div>
    </div>
	</div>

	<div class="row text-center">
		<div class="col-md-6 col-md-offset-3 ">
			<!-- Activate Simple Slider on your input -->
		  <input id="volumen" type="text" data-slider="true">
		</div>
	</div>



  <script>
    //$("#my-input").simpleSlider();
    $("#PlaySong").click( function(){

			$.get( "/music/play", function( data ) {
				$("#PlaySong").addClass("hidden");
				$("#PauseSong").removeClass("hidden");
				console.log( data );
				$("#title").text( data.name );
      });
			console.log("play");
    });

		$("#PauseSong").click( function(){
      $.get( "/music/pause", function( data ) {
				$("#PlaySong").removeClass("hidden");
				$("#PauseSong").addClass("hidden");
				console.log("pause...");
				console.log( data );
				$("#title").text( data.name );
      });
    });

    $("#BeforeSong").click( function(){
      $.get( "/music/prev", function( data ) {
        console.log("play...");
				console.log( data );
				$("#title").text( data.name );
      });
    });

    $("#NextSong").click( function(){
      $.get( "/music/next", function( data ) {
        console.log("play...");
				console.log( data );
				$("#title").text( data.name );
      });
    });

		$("#volumen").bind("slider:changed", function (event, data) {
		  // The currently selected value of the slider
		  //alert(data.value);
			value = Math.round( data.value*300 );
			console.log( "SOUND: " + value );

			$.get("/music/volume/"+value, function( data ){
				console.log("Ajuste..");
			});
		  // The value as a ratio of the slider (between 0 and 1)
		  //alert(data.ratio);
			console.log(data.ratio);
		});

  </script>
</body>
</html>
