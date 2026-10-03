
import subprocess
from google import genai


API_KEY = "AQ.Ab8RN6Jdfwut7Fo01SGAiYAaEkXt8qhAMRE40YQosU_wrGYl2w"
MODEL = "gemma-4-26b-a4b-it"


def run_tests():
    return subprocess.run(
        ["pytest", "-v"],
        cwd="codebase",
        capture_output=True,
        text=True,
    )


def ask_gemini(test_output):
    client = genai.Client(api_key=API_KEY)

    prompt = f"""You are an expert Python debugging engineer.

Our project tests have failed.

Here is the pytest output:

--- TEST OUTPUT ---
{test_output}
--- END TEST OUTPUT ---

Analyze the failure carefully.

Tell me:

1. ROOT CAUSE — What is actually causing the failure?
2. AFFECTED FILE — Which file is responsible?
3. AFFECTED FUNCTION — Which function, method, or class is responsible?
4. FAILURE FLOW — Explain briefly how the code reaches the failure.
5. RECOMMENDED FIX — What specific change should the developer make?
6. WHY IT WORKS — Why will this change fix the failure?
7. CONFIDENCE — High, Medium, or Low, and why.

Important:
- Focus only on the reported failure.
- Do not suggest unrelated improvements.
- Do not rewrite the project.
- Do not make changes yourself.
- Give a specific, actionable recommendation.
- If the pytest output does not contain enough information to determine the cause, clearly say what information is missing.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text


def main():
    print("🧪 Running tests...\n")

    result = run_tests()

    output = result.stdout + "\n" + result.stderr

    print(output)

    if result.returncode == 0:
        print("✅ ALL TESTS PASSED")
        return

    print("❌ TESTS FAILED")
    print("\n🤖 Sending failure to Gemini...\n")

    try:
        analysis = ask_gemini(output)

        print("🤖 GEMINI ANALYSIS:\n")
        print(analysis)

    except Exception as e:
        print(f"❌ Gemini error: {e}")


if __name__ == "__main__":
    main()
