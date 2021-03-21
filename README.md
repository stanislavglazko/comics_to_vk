# Comics publisher

My app downloads comic from https://xkcd.com/ and post it to your community in vk.
My app makes random choice from xkcd.com collection of comics, 
takes image and comment and make a post on the wall of your community. 

### How to install
Python3 should be already installed.

1) clone the repo
2) use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
    ```
    pip install -r requirements.txt
    ```
3) you must have an account, community and application in vk
   
4) add .env file in the directory of the tool:
    ```
    CLIENT_ID=<your_app_in_vk_id>
    ACCESS_TOKEN=<your_personal_access_token_in_vk>
    GROUP_ID=<your_comunity_in_vk_id>
    ```
   
### How to use
1) Write: 
    ```
    python3 main.py 
    ```
2) enjoy good content in your community

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).