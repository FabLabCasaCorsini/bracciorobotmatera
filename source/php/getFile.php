<?php

  $fileName = $_GET['file'];


  $source_file = '/var/www/appius/matera/gcodes/'.$fileName;
  $destination_path = '/var/www/appius/matera/old_files/';


  $fileList = '/var/www/appius/matera/gcode_files';

  $pagecontents = file_get_contents($source_file);
  echo $pagecontents;

  $fileListSource = file_get_contents($fileList);

  $fn = fopen($fileList,"r");
  $newFileContent = "";

  while(! feof($fn))  {
    $line = fgets($fn);
    if (!(strpos($line, $fileName) !== false))
      $newFileContent = $newFileContent.$line;
  }

  fclose($fn);

  $fn = fopen($fileList,"w");
  fwrite($fn, $newFileContent);
  fclose($fn);

  rename($source_file, $destination_path . pathinfo($source_file, PATHINFO_BASENAME));

?>
