from troubleshooting import Troubleshooter

troubleshooter = Troubleshooter()

test_text = "My computer won't turn on."

suggestion = troubleshooter.get_troubleshooting_suggestion(test_text)

print("\nTroubleshooting Suggestion:\n")
print(suggestion)

api_response = troubleshooter.raw_api_call(test_text)
print("\nRaw API Call: \n")
print(api_response)
