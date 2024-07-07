server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host "localhost";
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
    }
}