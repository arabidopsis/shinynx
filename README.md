# sticky nginx sessions and shiny

Test shiny and also nginx "stickyness".

If you want to self-host your py-shiny app and your frontend is nginx this repo
shows how to configure multiple shiny instances for the backend (to handle e.g. load).

Shiny uses websockets so of course if you are behind - say - a CloudFlare firewall then this might not work
at *all* unless websocket traffic has been enabled.

The shiny app is based on the [load balancer example](https://github.com/posit-dev/py-shiny/blob/7ba8f90a44ee25f41aa8c258eceeba6807e0017a/examples/load_balance/app.py) from the py-shiny github.

Run a foreground nginx process on port 8080

```bash
nginx -c $(realpath .)/sticky.conf
```
It assumes there are 4 unix socket endpoints `app{n}.sock` in this directory.

Now run multiple background shiny instances:

```bash
# starts 4 uvicorn processes holding one app.asgi:app shiny instance each
python -m shinyma.web --workers=4 app.asgi
```

You will see `app{n}.sock` files appear in this directory. These are the endpoints for each
of 4 shiny instances.

Shiny requires a "stickyness" i.e. it must always communicate with the *same* background
shiny instance. So the file `sticky.py` is the crucial enhancment required.

You can fire up multiple browser tabs to hit this website concurrently with:

```bash
# fire up 10 browser tabs
python -m shinyma.browser -n10
```

The nginx load balancer should ensure that the processes are "sticky" using a
random "sticky" cookie. There are possibly better solutions if you have the "plus" version of nginx. But
this works with the open source version.

see [the shiny docs](https://shiny.posit.co/py/docs/deploy-on-prem.html#other-hosting-options)

Since the cookie values are randomly generated, a restart of the backend without a restart of nginx
will envolve failures since cookie values have changed.

Currently we set our cookie *value* to the uvicorn endpoint value (e.g. `app1.sock` or `app2.sock` etc.).
**But** there is no guarantee that nginx will map a cookie value of `app1.sock` to the
`app1.sock` process (it's a hash after all!).
