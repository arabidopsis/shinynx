# shinytest

test shiny and also nginx stickyness

run foreground nginx process on port 8080

```bash
nginx -c $(realpath .)/sticky.conf
```

Now run multiple background shiny apps:

```bash
# starts 4 uvicorn processes holding one app.asgi:app each
python -m app.web
```

The nginx load balancer should ensure that the processes are "sticky" using a
random "sticky" cookie.

see [the shiny docs](https://shiny.posit.co/py/docs/deploy-on-prem.html#other-hosting-options)
