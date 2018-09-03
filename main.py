from pprint import pprint
from fbrecog import FBRecog
from bs4 import BeautifulSoup, Comment
from urllib.request import urlopen
import requests

'''
path = 'C:\Alexey Technion\ProjectB_Smart_Home\mypic.jpg'
access_token = 'EAAYeBD26ZAQkBAPZBBURrrKoaXaIGOsTVLGHl9cUh0NYCo8PkCl0WIvZCgE9V2zUESxlpsaVpTgZC7sjJuc9ltDZAFtRrxjrT0bj7u9MQGfqRFjzfAIGVSCZAOfGbLzinqZADjauLZCmUYZBYNOmZCWVZAmbRKVR5zFRj8ZCnfAvIDLO4GKKYVFS5mNXVVpcieSkbv4rjEcKqRoMOcdqkZCuyWDnZBrlTt9XmrYs4ZD'
cookies = 'sb=xDdxW6gnARIAtC4XMxe0BTwL; datr=xDdxW7Ne7c2Tg4zreHGGsN8H; locale=en_US; dpr=1.5; pl=n; spin=r.4202043_b.trunk_t.1534169873_s.1_v.2_; act=1534169897844%2F3; c_user=100027703129886; xs=3%3ADZ81QAh8MPsC6g%3A2%3A1534169906%3A13822%3A-1; fr=0TeCrTm3A0MBtwlTt.AWWu3NCJcvYikAivBG9oC_YCZPs.BbcTfE.Qp.Ftx.0.0.BbcZMy.; presence=EDvF3EtimeF1534169900EuserFA21B27703129886A2EstateFDutF1534169900866CEchFDp_5f1B27703129886F2CC; wd=1113x830'
fb_dtsg = 'AQH94-Qo091F:AQEa7lhShlER'

# Instantiate the recog class
recog = FBRecog(access_token, cookies, fb_dtsg)

# Recog class can be used multiple times with different paths
# mike = 123059741964232
#temp = recog.get_user_data('/me/friends?field')

#recognized = recog.recognize(path)
#friend_name = recognized[0]['name']

'''


USERNAME = 'alexey.khrom@gmail.com'
PASSWORD = '13579qaz'
PROTECTED_URL = 'https://www.facebook.com/asia.zhivov/likes?lst=1198688678%3A843054236%3A1535896155'


def login(session, email, password):
    '''
    Attempt to login to Facebook. Returns cookies given to a user
    after they successfully log in.
    '''

    # Attempt to login to Facebook
    response = session.post('https://m.facebook.com/login.php', data={ 'email': email, 'pass': password},
                            allow_redirects=False)

    assert response.status_code == 302
    assert 'c_user' in response.cookies
    return response.cookies


if __name__ == "__main__":

    session = requests.session()
    cookies = login(session, USERNAME, PASSWORD)
    response = session.get(PROTECTED_URL, cookies=cookies, allow_redirects=False)
    assert response.text.find('Home') != -1

    # to visually see if you got into the protected page, I recomend copying
    # the value of response.text, pasting it in the HTML input field of
    # http://codebeautify.org/htmlviewer/ and hitting the run button

    soup = BeautifulSoup(response.content, "html.parser")
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    final_likes_list = []
    for comment in comments:
        soup_inner = BeautifulSoup(comment, 'html.parser')
        div_likes_list = soup_inner.findAll('div',{'class':['fsl fwb fcb', 'fsl fwb fcb _5wj-']}) # one for eng. and one for heb.
        for div_like in div_likes_list:
            div_like_link = div_like.find('a')
            final_likes_list.append({div_like_link.text: div_like_link['href']})

    for liked_page in final_likes_list:
        print(liked_page)
