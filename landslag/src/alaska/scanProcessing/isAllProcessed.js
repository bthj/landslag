var walk = require('walk'),
  fs = require('fs'),
  options,
  walker;


var filesToAdd = [];
var filesInCollection = [];

fs.readdir('/media/bthj/tankur3/alaska/teikningar/vinnsla/png', function(err,files){
    for( i=0; i<files.length; i++ ) {
//        console.log(files[i]);
        filesInCollection.push(files[i]);    
    }
});

function checkIfNotInFinishedCollectionAndThenAdd( filename ) {
    var isInCollection = false;
    for( i=0; i<filesInCollection.length; i++ ) {
        if( filename == filesInCollection[i].split('.')[0] ) {
            isInCollection = true;
            break;
        }
    }
    if( false == isInCollection ) {
        filesToAdd.push( filename );
        console.log(filename);
    }
}


options = {
    followLinks: false,
    // filters: ["Temp", "_Temp"] // directories with these
                                  // keys will be skipped
};

walker = walk.walk("/media/bthj/tankur3/alaska/teikningar/vinnsla", options);

walker.on("file", function (root, fileStats, next) {
  fs.readFile(fileStats.name, function () {
    // doStuff
    
    if( root.indexOf('unnid') !== -1 && root.indexOf('AppleDouble') === -1 ) {
        if( fileStats.name.match(/tif$/) ) {
//          console.log( root + '---' + fileStats.name.split('.')[0]);
            checkIfNotInFinishedCollectionAndThenAdd( fileStats.name.split('.')[0] );            
        }
    }
    next();
  });
});


walker.on("end", function () {
  console.log("all done: " + filesToAdd.length);
});
