test:
	nginx -c $(realpath .)/templates/sticky.conf

WORKERS=2
nginx:
	footprint config template templates/nginx.conf -o shiny.conf server-name=shiny.plantenergy.org workers=$(WORKERS) module=app

systemd:
	footprint config template --user -o shiny.service templates/systemd.service workers=$(WORKERS) appname=app.core

.PHONY: nginx systemd test
