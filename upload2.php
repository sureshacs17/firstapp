
<!DOCTYPE html>
<html>
    <head>
    <title>PlantCV</title>
     <link rel="stylesheet" href="css/s12.css">
    </head>
    <body>
            <header>
             <div id="section1">
                 <nav class="nav">
                <div class="main">
                  <div class="p1">
                        <br><br><img src="imgs/p.png">
                    </div>
                    <ul>
                        <li> <a href="mode.html">BACK</a></li>
                        <li> <a href="index.php">HOME</a></li>
                        <li> <a href="gal.html">GALLERY</a></li>
                        <li> <a href="binder.html">BINDER</a></li>
                        <li> <a href="ab.html">ABOUT</a></li>
                    </ul>
                    </nav>
                     </div>
                <div class="c2">
                  <p><b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 
                  &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlant Phenotyping Using Computer Vision</b></p>
                </div>  

<div class="login-box">
<form name="form" method="post" action="upload2.php" enctype="multipart/form-data" >
 <input id="fileupload" class="btn" type='file' name='my_file' accept="image/*"  required/>
 <input type="submit" class="btn1"  name="submit" value="Upload"/ >
</form>

<?php
if (($_FILES['my_file']['name']!="")){
// Where the file is going to be stored
 $target_dir = "upload/input2/";
 $file = $_FILES['my_file']['name'];
 $path = pathinfo($file);
 $filename = $path['filename'];
 $ext = $path['extension'];
 $temp_name = $_FILES['my_file']['tmp_name'];

 $path_filename_ext = $target_dir.'input'.".".'jpg';

 move_uploaded_file($temp_name,$path_filename_ext);
 echo"<br><center><img src='upload/input2/input.jpg' height=250 width=300></center>";

}
?>
<br></br><form name="f1" method="post" action="action2.php" enctype="multipart/form-data" >
<center><input type="submit" class="btn2" value="Get Results" action="action.php"></center>
</form>
</div>
</header>
</body>
</html>

