var verify = function(uni) {
  if(uni.length == 7 | uni.length == 6) {
    if(uni.charAt(0)) {
      var swap = 3;
      
    } else {
      var swap = 2;
    }  
  } else {
    throw  "length is bad"
  }
  var xmlhttp;
  if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  } else {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      if(xmlhttp.responseText.indexOf(uni) > 0) {
        return true;
      } else {
        return false;
      } 
    }
  }
  xmlhttp.open("POST","https://directory.columbia.edu/people/uni",true);
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"); //text/html
  xmlhttp.send("code=" + uni);
}