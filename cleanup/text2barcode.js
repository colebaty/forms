var textValue = this.getField("24").value;

var regex = /\*?([^\*]*)\*?/;

var matches = textValue.match(regex);
console.println("matches.length: " + matches.length);
console.println("matches[1]: " + matches[1]);

if (matches && matches.length > 1) {
  var data = matches[1];
}

console.println("data: " + data);

//var barcodeFont = "Free 3 of 9 Regular";

//this.getField("24").textFont = barcodeFont;
if (data != "") {
  this.getField("24").value = "*" +  data + "*";
}
else {
  this.getField("24").value = "";
}
