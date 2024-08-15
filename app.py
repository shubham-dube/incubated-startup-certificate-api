from flask import Flask, jsonify, Response, make_response, request
import requests
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

@app.route("/api/v1/getCertificate", methods=["POST"])
def getCertificate():
    try:
        url = "https://api.startupindia.gov.in/sih/api/noauth/dpiit/services/validate/certificate"

        dipp = request.json.get("dippNumber")  #DIPP141531
        certType = request.json.get("certificateType")
        session = requests.Session()

        session.headers = {
            'authority': 'api.startupindia.gov.in',
            'method': 'POST',
            'path': '/sih/api/noauth/dpiit/services/validate/certificate',
            'scheme': 'https',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
            'Content-Length': '75',
            'Content-Type': 'application/json',
            'Origin': 'https://www.startupindia.gov.in',
            'Priority': 'u=1, i',
            'Referer': 'https://www.startupindia.gov.in/',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        postBody = {
            "certificateType": certType,
            "dippNumber": dipp,
            "entityName": ""
        }

        response = session.post(url, json=postBody)

        pdfLink = "https://recognition-be.startupindia.gov.in" + response.json()['data']

        jsonResponse = {
            "status": "Successfull",
            "pdfLink": pdfLink
        }

        return jsonify(jsonResponse)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching UDID Number Details"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=5001)