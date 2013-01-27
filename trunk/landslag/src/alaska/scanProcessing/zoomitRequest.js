var fs = require('fs'),
	request = require('request'),
	http = require('http');

var fileNames = new Array();
var currentFileIndex = 0;

fs.readdir('/Users/bthj/alaska/vinnsla/png', function(err, files){

	for( i=0; i<files.length; i++ ) {
		fileNames.push( files[i] );
		console.log( '#' + i + ': ' + files[i] );
	}

	oneZoomItGet( fileNames[currentFileIndex] );	
});




function oneZoomItGet( fileName ) {
	request.get( {
			url:'http://api.zoom.it/v1/content/?url=http://teikningar.alaska.is/png/' + fileName, 
			json:true
		}, 
		function(error, response, body){
			
			if( body ) {
				console.log( (body.url ? body.url : "NO URL") + " - ready: " + body.ready + ", failed: " + body.failed );
			} else {
				console.log("NOT READY FOR: " + fileNames[currentFileIndex] + ", lets retry...");
			}
			
			if( !body ) {
				setTimeout( function(){oneZoomItGet( fileNames[currentFileIndex] );}, 300000 );
			} else if( body.ready || body.failed ) {
				oneZoomItGet( fileNames[currentFileIndex++] );
			} else {
				setTimeout( function(){oneZoomItGet( fileNames[currentFileIndex++] );}, 300000 );
			}
		} 
	);
}




/*
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.write( JSON.stringify(fileNames) );
  res.end();
}).listen(1337, '127.0.0.1');
console.log('Server running at http://127.0.0.1:1337/');
*/