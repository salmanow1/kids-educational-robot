name: Educational Robot Daily Publisher

on:
  schedule:
    - cron: '0 14 * * *'
  workflow_dispatch:

jobs:
  build-and-run:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Video Tools and ImageMagick
      run: |
        sudo apt-get update
        sudo apt-get install -y ffmpeg imagemagick ttf-mscorefonts-installer fonts-liberation
        # سطر سحري لكسر حماية النظام والسماح لبرنامج الأتمتة بكتابة النصوص العربية
        sudo sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml

    - name: Install Dependencies
      run: |
        pip install gtts moviepy requests

    - name: Run Video Robot
      run: |
        python robot_free.py
