from flask import Flask, request, Response
import requests

app = Flask(__name__)
BLOCKED_HOST = "service-fb-examly-io-7tvaoi4e5q-uk.a.run.app"

@app.route("/", methods=["GET", "POST"])
def proxy():
    target_url = request.args.get("url")

    if not target_url:
        return Response("No URL provided", status=400)

    # Block requests to the specified host
    if BLOCKED_HOST in target_url:
        return Response("Blocked", status=403)

    # Forward request to the actual target
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for key, value in request.headers if key != "Host"},
            data=request.get_data(),
            allow_redirects=True
        )
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except requests.exceptions.RequestException:
        return Response("Error forwarding request", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8055)
