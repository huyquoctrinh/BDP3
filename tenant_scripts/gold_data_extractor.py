from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = ""

class GoldDataExtractor:
    def __init__(self):
        self.client = OpenAI()

    def process_prompt(self, prompts):
        print("Number of prompts:", len(prompts))
        instructions = f"Extract the mood label of these {len(prompts)} review and write it in 1 word (from these 3 words Neutral, Positive, Negative), place 1 line for each reviews."
        for prompt in prompts:
            instructions += f"\n{prompt}"

        return instructions

    def process_response(self, response):
        res = []
        for line in response.split("\n"):
            res.append(line.strip())
        return res

    def extract_gold_data(self, prompts):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": self.process_prompt(prompts)
                }
            ]
        )

        return self.process_response(completion.choices[0].message.content)

if __name__ == "__main__":
    extractor = GoldDataExtractor()
    print(extractor.extract_gold_data(
        [
            "A wonderful read, if you have the time, patience, and energy",
            "Infinite Jest: A Novel"
        ]
    ))

