<?php
$servername = "localhost";
$username = "voiceit2_kryptst";
$password = "MonHGPass101.";
$dbname = "voiceit2_roadtrip";

// Create connection
echo "index page accessed";
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}

$mainR = mysqli_query($conn, $sql);



mysqli_close($conn);
?>

