// CSVファイルのパス
const csvFilePath = '../data/data_with_ruby.csv';


function removeRuby(rubyHTML) {
    return rubyHTML.replaceAll(/<rt>.*?<\/rt>/g, '').replaceAll("<ruby>", "").replaceAll("</ruby>", "");
}

// CSVを読み込んでデータを表示
Papa.parse(csvFilePath, {
    download: true,
    header: true,
    complete: function(results) {
        const data = results.data;
        let pageDivs = '';
        let currentPages = '';
        let currentPage = '';
        let pageCounter = 0;
        let pagesCounter = 0;

        data.forEach((row, index) => {
            if(!row.名前) return;
            // 新しい.pageが6つ以上なら新しい.pagesに
            if (index === 6 || index === 12 || index === 17 || index === 23 || index === 29) {
                pageCounter++;
                if(pageCounter%2 == 1) {
                    currentPages += `
                        <div class="sidebar ${pageCounter > 3 ? 'east' : ''}">
                            <div class="sidebarMain">
                                <img src="../../assets/images/textbook/sidebar/${pageCounter > 3 ? '東軍' : '西軍'}.webp" alt="${pageCounter > 3 ? '東軍' : '西軍'}">
                            </div>
                            <div class="sidebarMargin"></div>
                        </div>
                    `;
                }
                currentPages += `
                    <div class="page ${pageCounter%2 == 1 ? 'leftPage' : 'rightPage'}">
                        <div class="topBlack">
                            ${pageCounter%2 == 1 ? `
                                <h2>クイズの<ruby>答<rt>こた</rt></ruby>えと<ruby>解説<rt>かいせつ</rt></ruby></h2>
                                <p><ruby>各人物<rt>かくじんぶつ</rt></ruby>の<ruby>紹介<rt>しょうかい</rt></ruby>ページの<ruby>下<rt>した</rt></ruby>にあるクイズの<ruby>答<rt>こた</rt></ruby>えと<ruby>解説<rt>かいせつ</rt></ruby>をまとめています。<ruby>全問<rt>ぜんもん</rt></ruby><ruby>正解<rt>せいかい</rt></ruby>で<ruby>関ヶ原<rt>せきがはら</rt></ruby>の<ruby>戦<rt>たたか</rt></ruby>いマスター！？</p>
                            ` : ''}
                        </div>
                        <div class="mainArea">
                            ${currentPage}
                        </div>
                    </div>
                `;
                if(pageCounter%2 == 0) {
                    currentPages += `
                        <div class="sidebar ${row.東西 === '東軍' ? 'east' : ''}">
                            <div class="sidebarMain">
                                <img src="../../assets/images/textbook/sidebar/${row.東西 === '東軍' ? '東軍' : '西軍'}.webp" alt="${row.東西}">
                            </div>
                            <div class="sidebarMargin"></div>
                        </div>
                    `;
                }
                currentPage = '';
            }

            // 新しい.pagesが12人以上なら新しい.pagesを作る
            if (index % 12 === 0 && index !== 0) {
                pagesCounter++;
                pageDivs += `<div class="pages" data-name="クイズQA${pagesCounter}.png">${currentPages}</div>`;
                currentPages = '';
            }

            // QAブロックの作成
            currentPage += `
                <div class="QA">
                    <div class="QATitle ${row.東西=='東軍' ? 'east' : ''}">Q.${row.番号} ${row.名前} p.${row.ページ}</div>
                    <div class="QAMain">
                        <div class="dialog">
                            <div class="dialogCharacter">
                                <img src="../../assets/images/textbook/mini_circle/gegw/${removeRuby(row.名前)}.webp" alt="" class="mini">
                                <div class="dialogCharacterName">${removeRuby(row.名前)}</div>
                            </div>
                            <p class="dialogContents Q">${row.質問}</p>
                        </div>
                        <div class="dialog">
                            <div class="dialogCharacter">
                                <img src="../../assets/images/textbook/common/mini/gegw/${row.回答キャラ}.webp" alt="" class="mini">
                                <div class="dialogCharacterName">${row.回答キャラ.slice(0, row.回答キャラ.length-1)}</div>
                            </div>
                            <p class="dialogContents">${row.回答}</p>
                        </div>
                        <div class="dialog">
                            <div class="dialogCharacter">
                                <img src="../../assets/images/textbook/mini_circle/gegw/${removeRuby(row.名前)}.webp" alt="" class="mini">
                                <div class="dialogCharacterName">${removeRuby(row.名前)}</div>
                            </div>
                            <p class="dialogContents">${row.解説}</p>
                        </div>
                    </div>
                </div>
            `;
        });

        // 最後のページを追加
        if (currentPage) {
            currentPages += `
                <div class="page rightPage">
                    <div class="topBlack"></div>
                    <div class="mainArea">
                        ${currentPage}
                    </div>
                </div>
                <div class="sidebar ${data[data.length - 2].東西 === '東軍' ? 'east' : ''}">
                    <div class="sidebarMain">
                        <img src="../../assets/images/textbook/sidebar/${data[data.length - 2].東西 === '東軍' ? '東軍' : '西軍'}.webp" alt="${data[data.length - 2].東西}">
                    </div>
                    <div class="sidebarMargin"></div>
                </div>
            `;
            pageDivs += `<div class="pages" data-name="クイズQA${pagesCounter+1}.png">${currentPages}</div>`;
        }

        // ページエリアに挿入
        document.querySelector('.pageArea').innerHTML = pageDivs;
    }
});