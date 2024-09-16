// メイン処理を実行するフォルダを指定します
var aiFolder = Folder.selectDialog(".epsファイルがあるフォルダを選択してください。");
var pngFolder = Folder.selectDialog(".pngファイルがあるフォルダを選択してください。");
if (aiFolder && pngFolder) {
    processFolder(aiFolder, pngFolder);
    alert("処理が完了しました。");
    // app.quit();
} else {
    alert("フォルダが選択されませんでした。");
    // app.quit();
}


var closeEachFile = false;


function processFolder(epsFolder, pngFolder) {
    var aiFolderFiles = epsFolder.getFiles();
    var pngFolderFiles = pngFolder.getFiles();

    // alert(aiFolderFiles.length);
    // alert(pngFolderFiles.length);

    var epsFiles = [];
    var pngFiles = [];

    for(var i = 0; i < aiFolderFiles.length; i++) {
        var file = aiFolderFiles[i];
        if(file instanceof File && file.name.match(/\.ai$/i)) {
            epsFiles.push(file);
        }
    }

    for(var i = 0; i < pngFolderFiles.length; i++) {
        var file = pngFolderFiles[i];
        if(file instanceof File && file.name.match(/\.png$/i)) {
            pngFiles.push(file);
        }
    }

    if(confirm("重くなるのを防ぐために、AIファイルを逐次閉じますか？")) {
        closeEachFile = true;
    }

    alert('epsファイルの数：' + epsFiles.length + ', pngファイルの数：' + pngFiles.length);

    var notFoundFiles = [];
    for (var i = 0; i < pngFiles.length; i++) {
        var pngFile = pngFiles[i];
        var found = false;
        for(var j = 0; j < epsFiles.length; j++) {
            var epsFile = epsFiles[j];
            if(epsFile.name.indexOf(pngFile.name.replace(".png", "")) > -1) {
                found = true;
                processFile(epsFile, pngFile);
                break;
            }
        }
        if(!found) {
            notFoundFiles.push(pngFile);
            // alert('「' + pngFile.name + '」に対応するaiファイルが見つかりませんでした。「' + pngFile.name.replace(".png", "") + '」を含むaiファイルがあるか確認してください。');
        }
    }
    if(notFoundFiles.length > 0) {
        var message = notFoundFiles.length + '個のpngファイルに対応するepsファイルが見つかりませんでした。';
        alert(message);
    }
}



// 処理を実行する関数
function processFile(epsFile, pngFile) {
    // ファイルを開く
    var doc = app.open(epsFile);

    // // 配置したい位置の座標（ポイント単位）


    // プリントパックのA5見開きサイズの、塗り足しを含め左上と右下の座標

    var left = 86.5
    var top = 57.5
    var right = 945.39
    var bottom = 669.79
    
    var width = right - left;
    var height = bottom - top;

    var x = left - (182.02 - 86.5) // なぜか182.02が左端になる
    var y = top - (124.02 - 57.5) // なぜか124.02が上端になる

    // alert('width: ' + width + ', height: ' + height + ', x: ' + x + ', y: ' + y);

    // 画像を配置するレイヤーを作成
    var imageLayer = doc.layers.getByName("レイヤー1");

    // 画像を配置
    // var pngFile = new File(imagePath);

    if (pngFile.exists) {
        var image = imageLayer.placedItems.add();
        image.file = pngFile;

        image.resize((width/image.width)*100, (height/image.height)*100);

        // alert('image.left: ' + image.left + ', image.top: ' + image.top);

        image.translate(x - image.left, -y - image.top);
        // image.translate(x - image.geometricBounds[0], y - image.geometricBounds[1]);
        image.embed();
    } else {
        alert("画像ファイルが見つかりませんでした。");
    }

    // 変更を保存して閉じる
    if(!doc.saved) {
        // var savePath = new File(epsFile.fullName.replace(".ai", ".pdf"));
        var savePath = new File(epsFile.fullName);
        // alert('savePath: ' + savePath);
        doc.saveAs(savePath);
    }

    if(closeEachFile) {
        doc.close();
    }
}



