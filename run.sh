#!/usr/bin/env bash
sudo adduser jenkins sudo
cd web;../tailwindcss -i static/styles/main.css -o static/styles/tailwind.css
python3 -m flask --app web run --host 0.0.0.0
