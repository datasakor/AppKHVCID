import streamlit as st
import requests

# appkhvcid.streamlit.com
# Define your Google reCAPTCHA keys
RECAPTCHA_SITE_KEY = "6LcIK7UqAAAAAARVxnk-mPYaL-UTHuyCwvsmyB7I"  # Replace with your Site Key
RECAPTCHA_SECRET_KEY = "6LcIK7UqAAAAAFglmjjcCcLgdjsLPW9QTJ3AVxpA"  # Replace with your Secret Key

# Function to verify reCAPTCHA response
def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": RECAPTCHA_SECRET_KEY, "response": token}
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get("success", False)

# Define your search function
def search_vac_info_detail(id_number, birthdate):
    # Dummy implementation for testing
    if id_number == "12345" and birthdate == "2000-01-01":
        return {"status": "success", "data": "Vaccination info found"}
    else:
        return {"status": "failure", "data": "No records found"}

# Streamlit app
def main():
    st.title("Vaccination Info Search")

    # Input fields
    id_number = st.text_input("Enter ID Number:")
    birthdate = st.date_input("Enter Birthdate:")

    # Embed reCAPTCHA widget and JavaScript
    st.components.v1.html(
        f"""
        <script src="https://www.google.com/recaptcha/api.js"></script>
        <div class="g-recaptcha" data-sitekey="{RECAPTCHA_SITE_KEY}" data-callback="recaptchaCallback"></div>
        <script>
        function recaptchaCallback(token) {{
            // Send the token to Streamlit via a hidden input
            const streamlitInput = window.parent.document.querySelectorAll("input[data-recaptcha='true']")[0];
            if (streamlitInput) {{
                streamlitInput.value = token;
                streamlitInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            }}
        }}
        </script>
        <input type="hidden" data-recaptcha="true">
        """,
        height=150,
    )

    # Read reCAPTCHA token from session state
    recaptcha_token = st.text_input("ReCAPTCHA Token", key="recaptcha_token", label_visibility="hidden")

    if st.button("Search"):
        if not recaptcha_token:
            st.error("Please complete the reCAPTCHA.")
        else:
            # Verify the token with Google
            is_valid_captcha = verify_recaptcha(recaptcha_token)
            if not is_valid_captcha:
                st.error("Invalid reCAPTCHA. Please try again.")
            else:
                # Perform the search
                result = search_vac_info_detail(id_number, birthdate.strftime("%Y-%m-%d"))
                if result["status"] == "success":
                    st.success(result["data"])
                else:
                    st.error(result["data"])

if __name__ == "__main__":
    main()appkhvcid.py
