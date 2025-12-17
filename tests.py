from alive_progress import alive_bar

def test_summary():
    with alive_bar(bar=None, title="Thinking...", spinner="dots_waves") as bar:
        from agent.utils import extract_visible_text
        import requests
        from agent.config import SUMMARY_MODEL, SUMMARY_CLIENT

        r = requests.get("https://weather.com/weather/tenday/l/USC+Los+Angeles+California?canonicalCityId=7d3c65d8b80674fb48647ddbc936bb8b")
        print("Text HTML:\n" + '-'*50 + "\n" + extract_visible_text(r.text)+ "\n" + '-'*50)
        query = "Find the current tempature in LA in the following text:\n"
        summary = SUMMARY_CLIENT.chat(model=SUMMARY_MODEL, messages=[{"role":"user", "content": query + extract_visible_text(r.text)}])
        print("Summary:\n" + '-'*50 + "\n" + summary.message.content + "\n" + '-'*50)

if __name__ == "__main__":
    test_summary()