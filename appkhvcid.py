import streamlit as st
import requests

# Domain name: appkhvcid.streamlit.app
# Define your Google reCAPTCHA keys
RECAPTCHA_SITE_KEY = "6LdjLrUqAAAAAKugEs1clSnzWyEv4HJDFDdCryvO"  # Replace with your Site Key
RECAPTCHA_SECRET_KEY = "6LdjLrUqAAAAAI0_TkjGwOjbmIPbj-SCAhUiyQt2"  # Replace with your Secret Key

# Function to verify reCAPTCHA response
def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": RECAPTCHA_SECRET_KEY, "response": token}
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get("success", False)

# Define your search function
def search_vac_info_detail(id_number, birthdate):
    # Ensure birthdate is properly formatted
    formatted_date = birthdate.strftime("%Y-%m-%d") if birthdate else None

    # Dummy implementation for testing
    if id_number == "12345" and formatted_date == "2000-01-01":
        return {"status": "success", "data": "Vaccination info found"}
    else:
        return {"status": "failure", "data": "No records found"}

# Streamlit app
def main():
    st.title("Vaccination Info Search")

    # Input fields
    id_number = st.text_input("Enter ID Number:")
    birthdate = st.date_input("Enter Birthdate:")


    st.components.v1.html(
    f"""
    <script src="https://www.google.com/recaptcha/enterprise.js?render={RECAPTCHA_SITE_KEY}"></script>
    <script>
      grecaptcha.ready(function() {{
        grecaptcha.execute("{RECAPTCHA_SITE_KEY}", {{action: 'submit'}}).then(function(token) {{
          window.parent.postMessage(token, "*");  // Send token to Streamlit
        }});
      }});
    </script>
    """,
    height=100,
    )

    st.components.v1.html(
        f"""
        <title>Title</title>
        <title>reCAPTCHA demo: Simple page</title>
        <script src="https://www.google.com/recaptcha/enterprise.js?render=6LdjLrUqAAAAAKugEs1clSnzWyEv4HJDFDdCryvO"></script>
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

    # Read reCAPTCHA token
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
                result = search_vac_info_detail(id_number, birthdate)
                if result["status"] == "success":
                    st.success(result["data"])
                else:
                    st.error(result["data"])

if __name__ == "__main__":
    main()
