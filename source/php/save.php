<?php

function gen_uuid() {
    return sprintf ( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x', mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0x0fff ) | 0x4000, mt_rand ( 0, 0x3fff ) | 0x8000, mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ) );
}

  $lines = $_POST['points'];
  $title = $_POST['title'];
  $fileName = $_POST['fileName'];
  $format = $_POST['format'];

  $folderPath = 'gcodes/';
	$tracks = explode("$$", $lines);


  if ($fileName == ''){
    $newFile = true;
    $name = $title;
  }
  else {
    $name = $fileName;
    $newFile = false;
  }

	$fileName = $name.".".$format;


  if (strcmp($format, "coord") == 0){
  	$myfileCoord = fopen($folderPath.$fileName, "w") or die("Unable to open file!");
  	fwrite($myfileCoord, $lines);
  	fclose($myfileCoord);
    exit(0);
  }

	$myfile = fopen($folderPath.$fileName, "w") or die("Unable to open file!");

	error_log ("filename = ".$fileName);

  $startCmd = "G21G90\n";
  $cmd = "G0";
  $cmdSpeed = "F10";

  fwrite($myfile, $startCmd);

  // abilito il relè
  $command = "M3"."\n";
  fwrite($myfile, $command);
  $command = "S0"."\n";
  fwrite($myfile, $command);

	foreach ($tracks as &$track) {

		$points =  explode("-", $track);

		for ($i = 0; $i < count($points); $i = $i + 2) {

		  error_log ("point ");
			$x = 85 - ($points[$i] + 5);
			$y = 85 - ($points[$i + 1] + 5);

			if ($i == 0){
				$command = $cmd."Z0"."X".$x."Y".$y.$cmdSpeed."\n";
				fwrite($myfile, $command);

        // accendo la lampada
        $command = "S1000"."\n";
        fwrite($myfile, $command);
			}

      $command = $cmd."Z0"."X".$x."Y".$y.$cmdSpeed."\n";
			fwrite($myfile, $command);

			if ($i == count($points) - 2){

        // spengo la lampada
        $command = "S0"."\n";
        fwrite($myfile, $command);


			}
		}

	}

  // disabilito il relè
  $command = "M5"."\n";
  fwrite($myfile, $command);

	fclose($myfile);


  if ($newFile == true){
  	$fileListFile = fopen("gcode_files", "a") or die("Unable to open file!");
  	fwrite($fileListFile, $fileName."\n");
  	fclose($fileListFile);
  }


?>
