import base64
import requests
import os

# OpenAI API Key
api_key = "YOUR API KEY"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def summarize_day(descriptions):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. You have received description of the screenshots from the user. You need to summarize the day."
            },
            {
                "role": "user",
                "content": "Summarize today's events. Format it nicely in bullet points in HTML. Your WHOLE answer must be in HTML."
            },
            {
                "role": "assistant",
                "content": "\n".join(descriptions)
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content']
    except:
        print(response.json())
        return ""



def get_image_content(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "What’s do you see? Be precise. You have the screenshots of my screen! Tell what you see on the screen and text you see in details! It can be rick and morty series, terminal, twitter, vs code, and other! answer with cool details! Answer in 20 words max! Make a story about my screenshot day out of it! If you can't see make best guess!"
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/png;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 50
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content']
    except:
        print(response.json())
        return ""

if __name__ == "__main__":
    results = []
    # folder_path = "/Users/robertlukoshko/Programming/demoday/screenshots"
    folder_path = "YOURSHONOTS FOLDER"

    for filename in sorted(os.listdir(folder_path)[:3]):
        if filename.endswith(".png"):
            print("working on: ", filename)
            image_path = os.path.join(folder_path, filename)
            result = get_image_content(image_path)
            if result:
                results.append(get_image_content(image_path))
            else:
                break

        

    for result in results:
        print(result)
    
    print("summarizing day")
    summary = summarize_day(results)

    print(summary)
    # save it to a file
    from datetime import date
    today = date.today()
    # summary_dir = "/Users/robertlukoshko/Programming/demoday/summary"
    summary_dir = "YOU SUMMARY FOLDER"
    if not os.path.exists(summary_dir):
        os.makedirs(summary_dir)
    with open(f"{summary_dir}/summary_{today}.txt", "w") as f:
        f.write(summary)


    import requests

    # webhook_url = "https://maker.ifttt.com/trigger/summary/with/key/hOLXS-"
    webhook_url = "Your IFTTT WEBHOOK URL"
    data = {"value1": summary}
    requests.post(webhook_url, json=data)
