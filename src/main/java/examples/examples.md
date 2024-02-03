<host> should be replaced by the backend domain\
Invalid JSON: curl -X POST --insecure -H "Content-type: application/json" -d 'x' "https://<host>:8080/describe" \
Schema validation error: curl -X POST --insecure -H "Content-type: application/json" -d '{"x": "y"}' "https://<host>:8080/describe" \
Not an image: curl -X POST --insecure -H "Content-type: application/json" -d '{"image": "kapsas", "language": "EN"}' "https://<host>:8080/describe" \
Correct request but couldn't detect any faces: curl -X POST --insecure -H "Content-type: application/json" -d @nofaces.txt "https://<host>:8080/describe" \
Correct request: curl -X POST --insecure -H "Content-type: application/json" -d @face.txt "https://<host>:8080/describe"

