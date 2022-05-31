// 모듈 설치 선행
// npm install puppeteer
// npm install dotenv
const puppeteer = require("puppeteer"); 
const dotenv = require("dotenv");
dotenv.config();

const login = async() => {
    try{
        const browser = await puppeteer.launch({headless: false, args:['--window-size=1920, 1080']});
        const page = await browser.newPage();
        await page.setViewport({
            width:1920,
            height:1080
        });
        // 이동할 URL
        await page.goto('https://facebook.com');

        //.env 파일을 사용해 보안에 신경씀
        const id = process.env.EMAIL;
        const password = process.env.PASSWORD;
        console.log(id);
        console.log(password);
        
        /*
        await page.evaluate((id, password) => {
            document.querySelector("#email").value = id;
            document.querySelector("#pass").value = password;
            document.querySelector("button[type=submit]").click();
        }, id, password)
        */

        await page.type("#email", id);
        await page.type("#pass", password);
        // 크롬 권한 요청
        await page.hover("button[type=submit]");
        await page.waitFor(3000);
        await page.click("button[type=submit]");
        await page.waitFor(10000);
        await page.keyboard.press("Escape");

    }catch(err){
        console.log(err);
    }
}

module.exports = login;
