// メイン処理を実行するフォルダを指定します
var aiFolder = Folder.selectDialog(".epsファイルがあるフォルダを選択してください。");
if (aiFolder) {
    processFolder(aiFolder);
    alert("処理が完了しました。");
    // app.quit();
} else {
    alert("フォルダが選択されませんでした。");
    // app.quit();
}


var closeEachFile = false;


function processFolder(epsFolder) {
    var aiFolderFiles = epsFolder.getFiles();

    var epsFiles = [];

    for(var i = 0; i < aiFolderFiles.length; i++) {
        var file = aiFolderFiles[i];
        if(file instanceof File && file.name.match(/\.eps$/i)) {
            epsFiles.push(file);
        }
    }

    alert('epsファイルの数：' + epsFiles.length);

    for(var i = 0; i < epsFiles.length; i++) {
        var doc = app.open(epsFiles[i]);
        var filePath = new File(epsFiles[i].fullName.replace(".eps", ".ai"));
        doc.saveAs(filePath);
        doc.close();
    }
}