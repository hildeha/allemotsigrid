import streamlit as st
import snowflake.connector


def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://addons-media.operacdn.com/media/CACHE/images/themes/05/144705/1.0-rev1/images/0993404e-79e0-4052-923d-89236e7c102f/ce42ef837a89c852c000eafd63cd0763.jpg");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

def main():

    st.set_page_config(page_title='Alle Mot Sigrid', page_icon=':fairy:',
                       layout='wide', initial_sidebar_state='auto')

    set_bg_hack_url()

    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    @st.experimental_singleton(suppress_st_warning=True)
    def init_connection():
        return snowflake.connector.connect(**st.secrets["snowflake"])

    conn = init_connection()

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    rows = run_query("SELECT * from oppgavesvar;")

    # Print results.
    for row in rows:
        st.write(f"{row[0]} has a :{row[1]}:")

    st.write("Add a new name and number to the database")
    name = st.text_input("Name")
    number = st.text_input("Number")

    if st.button("Submit"):
        run_query(f"INSERT INTO oppgavesvar (name, number) VALUES ('{name}', '{number}');")


if __name__ == '__main__':
    main()
