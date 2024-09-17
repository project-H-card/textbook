// function removeRuby(rubyHTML) {
//     return rubyHTML.replaceAll(/<rt>.*?<\/rt>/g, '').replaceAll("<ruby>", "").replaceAll("</ruby>", "");
// }

function pageNumber2mark(pageNumber) {
    switch (pageNumber) {
        case 1: return "①";
        case 2: return "②";
        case 3: return "③";
    }
}


// ページ番号をカウントするための変数
let pageNumber = 1;
let currentPageHalf = 'leftPageLeft';  // 左ページの左半分からスタート

// 挿入先の要素を取得
const main = document.querySelector('.pageArea');

// ページを挿入する関数
const insertPage = (content) => {
    const pageHtml = `
    <div class="pages" data-name="関ヶ原の戦いとは${pageNumber}.png">
        <div class="innerFrame"></div>
        <div class="mainFrame"></div>

        <div class="sidebar black"></div>

        <div class="page leftPage">
            <div class="topBlack">
                <h2><ruby>関ヶ原<rt>せきがはら</rt></ruby>の<ruby>戦<rt>たたか</rt></ruby>いとは${pageNumber2mark(pageNumber)}</h2>
            </div>
            <div class="mainArea">
                <div class="mainHalfArea">
                    ${content.leftPageLeft || ''}
                </div>
                <div class="separator"></div>
                <div class="mainHalfArea">
                    ${content.leftPageRight || ''}
                </div>
            </div>
        </div>

        <div class="page rightPage">
            <div class="topBlack"></div>
            <div class="mainArea">
                <div class="mainHalfArea">
                    ${content.rightPageLeft || ''}
                </div>
                <div class="separator"></div>
                <div class="mainHalfArea">
                    ${content.rightPageRight || ''}
                </div>
            </div>
        </div>
        <div class="sidebar black"></div>
    </div>`;

    main.insertAdjacentHTML('beforeend', pageHtml); // ページをmainに挿入
    pageNumber++;
};

// メインデータのHTMLを生成
const generateMainData = (data) => {
    let currentContent = {
        leftPageLeft: '',
        leftPageRight: '',
        rightPageLeft: '',
        rightPageRight: ''
    };

    data.forEach(item => {
        console.log(item);
        let html = '';
        switch (item.種類) {
            case 'dialog':
                html = `
                <div class="dialog">
                    <div class="dialogCharacter">
                        <img src="../../assets/images/textbook/common/mini/gegw/${item.キャラクター}.webp" alt="" class="mini">
                        <div class="dialogCharacterName">${item.キャラクター.slice(0,item.キャラクター.length-1)}</div>
                    </div>
                    <p class="dialogContents">${item.テキスト}</p>
                </div>`;
                break;
            case 'image':
                html = `<img src="../../assets/images/textbook/gegw/war/${item.画像}.webp" alt="" class="warImage">`;
                break;
            case 'title':
                html = `<h2 class="sectionTitle">${item.テキスト}</h2>`;
                break;
        }

        // データをページの対応する場所に割り当て
        currentContent[currentPageHalf] += html;

        if (item.種類 === 'split') {
            currentPageHalf = getNextPageHalf(currentPageHalf);
            // 全ページ分の半分にデータが揃った場合はページを挿入しリセット
            if (currentPageHalf === 'leftPageLeft') {
                insertPage(currentContent); // ページ全体を挿入
                currentContent = { leftPageLeft: '', leftPageRight: '', rightPageLeft: '', rightPageRight: '' }; // 初期化
            }
        }

    });

    // 最後に残ったデータを挿入
    if (currentContent.leftPageLeft || currentContent.leftPageRight || currentContent.rightPageLeft || currentContent.rightPageRight) {
        insertPage(currentContent);
    }
};

// 次のページ半分を取得する関数
const getNextPageHalf = (currentHalf) => {
    switch (currentHalf) {
        case 'leftPageLeft': return 'leftPageRight';
        case 'leftPageRight': return 'rightPageLeft';
        case 'rightPageLeft': return 'rightPageRight';
        case 'rightPageRight': return 'leftPageLeft';
    }
};

const csvFilePath = '../data/data_with_ruby.csv';
// 実行する
Papa.parse(csvFilePath, {
    download: true,
    header: true,
    complete: function(results) {
        generateMainData(results.data);

        const dialogs = document.querySelectorAll(".dialog");
        dialogs.forEach(dialog => {
            const dialogContents = dialog.querySelector(".dialogContents");
            const dialogContentsText = dialogContents.innerHTML.replaceAll(/<rt>.*?<\/rt>/g, '').replaceAll("<ruby>", "").replaceAll("</ruby>", "");
            if (dialogContentsText.length <= 48) {
                dialog.classList.add("shortText");
            }
        });

        // 最後の .topBlack の中に <h2>関ヶ原古戦場</h2>を追加
        const topBlacks = document.querySelectorAll(".topBlack");
        topBlacks[topBlacks.length - 1].innerHTML = '<h2><ruby>関ヶ原古戦場<rt>せきがはらこせんじょう</rt></ruby></h2>';
        
    }
});