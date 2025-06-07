const data = [...document.getElementsByClassName("honorWrap___BHau4")].map((e) => {
    const name = [...e.querySelectorAll(".honor-text")].find((el) => !el.classList.contains("honor-text-svg"))?.textContent.trim() || "Unknown";
    const stats = e.querySelector(".iconStats")?.textContent?.trim() || "Unknown";
    const playerid = e.querySelector(".linkWrap___ZS6r9")?.getAttribute("href").split("=")[1] || "Unknown";

    return { name, stats, playerid };
});

const encoded = btoa(JSON.stringify(data));
const textarea = document.createElement("textarea");
textarea.value = encoded;
document.body.appendChild(textarea);
textarea.select();
document.execCommand("copy");
document.body.removeChild(textarea);
alert("BSP Scrape successful, Profile links in Clipboard");
