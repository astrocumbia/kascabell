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
  <script src="public/bootstrap/js/simple-slider.js"></script>
  <link href="public/bootstrap/css/simple-slider.css" rel="stylesheet" type="text/css" />

  <title>Bienvenido</title>
</head>
<body>

<div class="row">
	<div class="col-md-offset-4 col-md-4">

		<form action="/upload" method="post" enctype="multipart/form-data">
			<div class="form-group">
				<label for="idSong">song</label>
				<input type="file" id="song" name="song" />
				<p class="help-block">Example block-level help text here.</p>
			</div>

			<div class="form-group">
				<label for="idCover">Cover</label>
				<input type="file" id="cover" name="cover" />
				<p class="help-block">Example block-level help text here.</p>
			</div>

			<button type="submit" class="btn btn-default">Submit</button>
		</form>
	</div>
</div>


</body>
</html>
