[...document.querySelectorAll(".skillExplain")].forEach((e, index) => {
    // console.log(e.textContent);
    if(e.textContent === "") {
        [...document.querySelectorAll(".aboutSkillContent")][index].innerHTML = "";
        console.log(index);
    }
});


downloadStatus = document.querySelector("#downloadStatus");

async function trySaveIMG(elem, path) {
    try {
        const dl = document.createElement("a");
        dl.href = await domtoimage.toPng(elem, {
            width: elem.clientWidth,
            height: elem.clientHeight
        });
        dl.download = path;
        dl.click();
    } catch(e) {
        console.log(`${path}のダウンロードに失敗。`);
    }
}

document.querySelector("#downloadButton").addEventListener("click", async (e) => {
    const pageElements = [...document.querySelectorAll(".page")];
    const pageNum = pageElements.length;

    // const loadErrorImageNames = loadErrorImages.map((path) => decodeURI(path.split("/").pop()));

    // const confirmResult = confirm(`${pageNum}枚の画像をダウンロードします。\n${loadErrorImageNames.length > 0 ? `以下の画像は読み込みに失敗しているため、デフォルト画像で代用します。\n${loadErrorImageNames.join("\n")}` : ""}`);
    const confirmResult = confirm(`${pageNum}枚の画像をダウンロードします。`);
    if(!confirmResult) return;

    // if(rate !== 30) {
    //     const rateConfirmResult = confirm(`画質は${rate}です。最終確認と入稿時は "30" を推奨していますがよろしいですか？`);
    //     if(!rateConfirmResult) return;
    // }
    // document.querySelectorAll(".cardContents").forEach((e) => e.style.border = "none");

    downloadStatus.classList.add("active");

    const batchSize = 4;
    let tasks = [];
    for(let i in pageElements) {
        const elem = pageElements[i];
        const filename = elem.dataset?.name || `page${String(i).padStart(3, '0')}.png`;
        // const filename = elem.dataset?.filename ? `card${String(i).padStart(3, '0')}_${elem.dataset?.filename}` : `card${String(i).padStart(3, '0')}.png`;
        console.log(filename);
        tasks.push(trySaveIMG(elem, filename));
        if(tasks.length >= batchSize) {
            await Promise.all(tasks);
            tasks = [];
            downloadStatus.innerHTML = `<span>${+i+1}/${pageNum}枚完了</span>`
        }
    }
    if(tasks.length > 0) {
        await Promise.all(tasks);
    }

    downloadStatus.innerHTML = `<span>${pageNum}枚全て完了</span>`;

    setTimeout(() => {
        alert(`${pageNum}枚の画像を全てダウンロードしました。`);
        downloadStatus.classList.remove("active");
        // document.querySelectorAll(".cardContents").forEach((e) => e.style.border = "white solid 1px");
    }, 3000);
})