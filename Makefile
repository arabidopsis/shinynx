nginx:
	nginx -c $(realpath .)/sticky.conf

.PHONY: nginx
