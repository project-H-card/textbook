function countNoRubyLength(str) {
    return str.replaceAll(/<rt>.*?<\/rt>/g, "")
        .replaceAll("<ruby>", "")
        .replaceAll("</ruby>", "")
        .length;
}

document.querySelectorAll(".skillTitle > span").forEach((e) => {
    if(countNoRubyLength(e.innerHTML) > 8) {
        console.log(e.innerHTML);
        e.classList.add("veryLong");
    } else if(countNoRubyLength(e.innerHTML) > 6) {
        console.log(e.innerHTML);
        e.classList.add("long");
    }
});