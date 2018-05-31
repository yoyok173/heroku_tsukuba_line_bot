import os
import sys
# noinspection PyPackageRequirements
import errno
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from richmenu import RichMenuManager, RichMenu

if os.path.isfile('.env') or os.path.isfile('env'):
    print('found .env. So it should be a local environment.')
    ENV = load_dotenv('.env')
    if ENV is None:
        ENV = load_dotenv('env')
else:
    print('Cannot find .env. So it should be on the cloud.')

CHANNEL_SECRET = os.getenv('2aeccaa784bd1a4d7f86f6516d91851a')
CHANNEL_ACCESS_TOKEN = os.getenv('3Qkr3SNlqPpzhZ0FYrPZupD/TcYAxK0+Kdh7J0u3JzH2qQkzZVGVjivLQ32olTcPIWOPg/jSaRvyekXU3gsLRs5BLHgCZEw1sHcTZoEy8yMOnTuXGvqh+27/RHYrQHVjTibPpU/YsK+qDXR+mrgEEQdB04t89/1O/w1cDnyilFU=')

if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# change below if using line-simulator or it would not work
# debugging_tool = 'line-sim'
debugging_tool = 'phone'

if debugging_tool == 'phone':
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
elif debugging_tool == 'line-sim':
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN, "http://localhost:8080/bot")


static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

rmm = RichMenuManager(CHANNEL_ACCESS_TOKEN)

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


def get_text_template_for_id():
    text = '''本人確認書類とは：
    
運転免許証・旅券・写真付き住基カード・個人番号カードなど１点、
または健康保険証&診察券など２点、または聞き取り'''
    return TextSendMessage(text=text)


def get_text_template_for_delegate():
    text = '''委任状とは：
「誰に」「どんな手続きを委任したか」を具体的に明記されていない場合や捺印のない場合はお受けできないことがございます。代筆による委任状の場合、拇印が必要です。詳細は市ホームページを御覧ください。'''
    return TextSendMessage(text=text)
