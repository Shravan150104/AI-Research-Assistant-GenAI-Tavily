import google.generativeai as genai
import requests

GEMINI_API_KEY = "AIzaSyAY2XLyAyGQpinjDxVWlo5iQT8nfPqNmno"
TAVILY_API_KEY = "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"

genai.configure(api_key=GEMINI_API_KEY)

def search_tavily(query):
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "search_depth": "advanced",
        "max_results": 5
    }
    response = requests.post("https://api.tavily.com/search", headers=headers, json=data)
    return response.json()

def format_tavily_results(results_json):
    formatted_text = ""
    for idx, result in enumerate(results_json["results"]):
        formatted_text += f"{idx+1}. {result['content']} (Source: {result['url']})\n\n"
    return formatted_text

def ask_gemini(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    chat = model.start_chat(
        history=[
            {"role": "user", "parts": ["You are an expert research assistant. Read the following search results and create a simple, clean, updated summary. Keep it short and professional."]}
        ]
    )

    response = chat.send_message(prompt)
    return response.text

def main():
    print("\n🤖 Welcome to the AI Research Bot!")
    subject = input("Enter a subject to research: ").strip()

    if not subject:
        print("❌ No subject entered. Exiting.")
        return

    print("\n🔎 Fetching latest news and updates...\n")
    search_results = search_tavily(subject)

    if "results" not in search_results or not search_results["results"]:
        print("❌ No search results found. Try a different topic.")
        return

    formatted_info = format_tavily_results(search_results)

    final_prompt = f"Here are some recent search results about '{subject}':\n\n{formatted_info}\n\nSummarize the latest developments in simple language."

    summary = ask_gemini(final_prompt)

    print("\n✅ AI SUMMARY:")
    print(summary)

    print("\n🌐 SOURCES USED:")
    for idx, result in enumerate(search_results["results"]):
        print(f"{idx+1}. {result['url']}")

if __name__ == "__main__":
    main()
