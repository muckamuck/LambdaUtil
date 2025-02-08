#### Run locally:
```
docker run -d --rm -p 9000:8080 simple-example-function
```

---

#### Invoke locally:
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"x": 42}'
```
