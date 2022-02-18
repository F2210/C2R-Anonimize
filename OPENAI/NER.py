import openai

openai.api_key = "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"

restart_sequence = "\n"

primer = open("primer.txt").read()

labels = ["person", "organisation", "location"]

labels = "".join([i + ", " for i in labels])

sentences = [
  "Jacco is studying at Utrecht University.",
  "Dan is an old friend from my time at Princeton.",
  "My back problems started to come back."
]

for sentence in sentences:

  input_text = "[" + labels + "]:" + sentence

  response = openai.Completion.create(
          engine="curie",
          prompt=primer + input_text,
          max_tokens=256,
          temperature=0.4,
          logprobs=4,
          stop="]",
      )

  # print(response)

  string = response["choices"][0]["text"].strip() + "]"

  # print("##################" + string + "##################")
