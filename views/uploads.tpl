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
