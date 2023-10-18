Invalid JSON: curl -X POST --insecure -H "Content-type: application/json" -d 'x' "https://localhost:8080/describe"
Schema validation error: curl -X POST --insecure -H "Content-type: application/json" -d '{"x": "y"}' "https://localhost:8080/describe"
Not an image: curl -X POST --insecure -H "Content-type: application/json" -d '{"image": "kapsas"}' "https://localhost:8080/describe"
Correct request: curl -X POST --insecure -H "Content-type: application/json" -d @req.txt "https://localhost:8080/describe"
