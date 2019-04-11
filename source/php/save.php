<?php

function gen_uuid() {
    return sprintf ( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x', mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0x0fff ) | 0x4000, mt_rand ( 0, 0x3fff ) | 0x8000, mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ) );
}


    $lines = $_POST['points'];
    $title = $_POST['title'];
    $fileName = $_POST['fileName'];

    $folderPath = 'gcodes/';
	$tracks = explode("$$", $lines);


  if ($fileName == ''){
    $newFile = true;
    $name = $title.'-_-'.gen_uuid();
  }
  else {
    $name = $fileName;
    $newFile = false;
  }

	$fileName = $name.".gcode";
	$fileNameCoord = $name.".coord";

	$myfileCoord = fopen($folderPath.$fileNameCoord, "w") or die("Unable to open file!");
	fwrite($myfileCoord, $lines);

	$myfile = fopen($folderPath.$fileName, "w") or die("Unable to open file!");

	error_log ("filename = ".$fileName);


  $startCmd = "G21G90\n";
  $cmd = "G0";
  $cmdSpeed = "F10";


  fwrite($myfile, $startCmd);

	foreach ($tracks as &$track) {

		$points =  explode("-", $track);

		for ($i = 0; $i < count($points); $i = $i + 2) {

		  error_log ("point ");
			$x = $points[$i];
			$y = $points[$i + 1];

			if ($i == 0){
				$command = $cmd."Z0"."X".$x."Y".$y.$cmdSpeed."\n";
				fwrite($myfile, $command);
			}

      $command = $cmd."Z1"."X".$x."Y".$y.$cmdSpeed."\n";
			fwrite($myfile, $command);

			if ($i == count($points) - 2){
        $command = $cmd."Z0"."X".$x."Y".$y.$cmdSpeed."\n";
				fwrite($myfile, $command);
			}
		}
	}

	fclose($myfile);
	fclose($myfileCoord);

  if ($newFile == true){
  	$fileListFile = fopen("gcode_files", "a") or die("Unable to open file!");
  	fwrite($fileListFile, $fileName."\n");
  	fclose($fileListFile);
  }


?>
