import google.generativeai as genai

genai.configure(api_key="AIzaSyAbxkexpVDG8MzpiptSlD-DqVBZ0OTyEMQ")

model = genai.GenerativeModel("gemini-1.5-pro")

try:
    response = model.generate_content("Say hello world")
    print(response.text)
except Exception as e:
    print("Gemini API error:", e)
