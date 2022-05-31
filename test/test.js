// 언어 분석 기술 문어/구어 중 한가지만 선택해 사용
// 언어 분석 기술(구어)
var openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken";
 
var access_key = 'fa776eba-2bca-4bed-84b9-2a2f9df8e111';
var analysisCode = 'ner';
//var text = 'YOUR_SENTENCE';
 
// 언어 분석 기술(구어)
var text = "11월 27일 서울시 강남구 월~금";
 
var requestJson = {
    'access_key': access_key,
    'argument': {
        'text': text,
        'analysis_code': analysisCode
    }
};
 
var request = require('request');
var options = {
    url: openApiURL,
    body: JSON.stringify(requestJson),
    headers: {'Content-Type':'application/json; charset=UTF-8'}
};
request.post(options, function (error, response, body) {
    console.log('responseCode = ' + response.statusCode);
    console.log('responseBody = ' + body);
});