import os
import google.generativeai as genai
import variables


def getResponse(command):
    model = genai.GenerativeModel(variables.geminiModel)
    genai.configure(api_key=variables.geminiApiKey)
    response = model.generate_content(variables.systemPrompt+" "+command,generation_config = genai.GenerationConfig(
            max_output_tokens=200,
            temperature=1,
        ), stream=True)
    return response
    # for chunk in response:
    #     print(chunk.text)
