import requests
import time
import telegram

API_KEY = "13eff20aca36e0dd3455c7ae1faca58f"
TELEGRAM_TOKEN = "7486864029:AAFYrEsL3pdPpXukZTLMCytTedTGr2OiA48"
TELEGRAM_CHAT_ID = "@Mateeusmedeiros"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_odds():
    url = "https://v3.football.api-sports.io/odds?league=71&season=2024&bookmaker=6"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("response", [])
    else:
        return []

def check_surebets():
    odds = get_odds()
    mensagens = []
    for match in odds:
        try:
            teams = match["teams"]
            bets = match["bookmakers"][0]["bets"]
            for bet in bets:
                if "Over/Under" in bet["name"]:
                    mensagens.append(f"{teams['home']['name']} x {teams['away']['name']} - {bet['name']}")
        except Exception:
            continue

    if mensagens:
        texto = "💰 Surebet Encontrada:\n\n" + "\n".join(mensagens)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=texto)

if __name__ == "__main__":
    while True:
        check_surebets()
        time.sleep(300)  # 5 minutos
