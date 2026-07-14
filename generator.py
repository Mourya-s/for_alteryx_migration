import json
import os
from google import genai

print("USING NEW FILE")
print("FILE =", os.path.abspath(__file__))

# Gemini API Key

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# Read workflow JSON
with open("generated/workflow.json", "r", encoding="utf-8") as f:
    workflow = json.load(f)

# Prompt
prompt = f"""
Convert this Alteryx workflow.

Return ONLY valid JSON.

Requirements:

1. Generate production-ready PySpark code.
2. Generate a COMPLETE Databricks Asset Bundle.
3. Include:
   - databricks.yml
   - resources/jobs.yml
4. Use DAB best practices.
5. Use include: resources/*.yml.
6. Include a dev target.
7. Use spark_python_task.
8. Do not use markdown.
9. Do not return explanations.
10. Return only JSON.

Schema:

{{
  "pyspark_code": "",
  "databricks_yml": "",
  "jobs_yml": ""
}}

Workflow:
{json.dumps(workflow, indent=2)}
"""

# Call Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# Save raw response
with open("generated/llm_output.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("LLM output saved.")

# Parse returned JSON
result = json.loads(response.text)

# Generate files
os.makedirs("generated/src", exist_ok=True)
os.makedirs("generated/resources", exist_ok=True)

with open("generated/src/workflow.py", "w", encoding="utf-8") as f:
    f.write(result["pyspark_code"])

with open("generated/databricks.yml", "w", encoding="utf-8") as f:
    f.write(result["databricks_yml"])

with open("generated/resources/jobs.yml", "w", encoding="utf-8") as f:
    f.write(result["jobs_yml"])

print("Generated:")
print("  generated/src/workflow.py")
print("  generated/databricks.yml")
print("  generated/resources/jobs.yml")