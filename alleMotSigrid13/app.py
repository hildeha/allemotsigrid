import streamlit as st
import snowflake.connector
from plotly.graph_objs import Layout, Figure
import plotly.graph_objects as go


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
    #@st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


    def print_oppgave(input_element, oppgavenummer):
        tittel, tekst, slider = input_element
        st.header(tittel)
        st.subheader(tekst)
        sliderverdi = st.slider(tittel, slider[0], slider[1], key=tittel)

        if st.button('Lås svar', key=str(slider)+tittel):
            run_query("INSERT INTO allemotsigrid VALUES (%s, %s, %s);" % (st.session_state[navn], oppgavenummer, sliderverdi))

    def get_new_ys(liste):
        sorted_index = []

        for first_indx, number in enumerate(set(liste)):
            counter = 0
            for indx, num in enumerate(liste):

                if num == number:
                    sorted_index.append((indx, counter))
                    counter += 1
        return [x[1] for x in sorted(sorted_index, key=lambda x: x[0])]

    def plot(xs, fasit, navn):
        colors = ['salmon' for x in xs]
        sizes = [10 for x in xs]
        fig_input = Figure(go.Scatter(x=xs, y=get_new_ys(xs),
                                      mode="markers+text",
                                      marker={'color': colors[i], 'size': sizes[i]},
                                      text=navn,
                                      textposition="bottom center",
                                      textfont={'color': 'salmon', 'size': 20}
                                      ))

        fig_input.add_trace(go.Scatter(x=[fasit], y=[0],
                                       mode='markers',
                                       marker={'color': 'yellow', 'size': 50},
                                       text='Fasit',
                                       textposition="top center",
                                       textfont={'color': 'salmon', 'size': 20}
                                       ))

        layout = Layout(paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        width=900, height=300,
                        )

        fig = Figure(data=fig_input.data, layout=layout)

        fig.add_hline(y=0, line_width=5, line_color="salmon")
        fig.update_xaxes(showticklabels=False, showgrid=False, showline=False)
        fig.update_yaxes(showticklabels=False, showgrid=False, showline=False)
        fig.update_layout(showlegend=False)

        return fig


    titler = ['Oppgave 1', 'Oppgave 2', 'Oppgave 3', 'Oppgave 4', 'Oppgave 5']


    tekster = ['dette er en oppgave for 1',
                 'dette er den andre oppgaven',
                 'tredje oppgave kommer her',
                 'fjerde oppgave på GGGGGG',
                 'her er femte og siste oppgave']

    slider_vals = [(0, 5), (0, 10), (0, 20), (0, 30), (0, 40)]

    if 'counter' not in st.session_state:
        st.session_state['counter'] = 0

    if 'navn' not in st.session_state:
        st.header('Velkommen til alle mot Sigrid, men hvem eeer du???')
        st.markdown('<br><br>', unsafe_allow_html=True)
        navn = st.text_input('Skriv inn navnet ditt under:')
        if navn is not '':
            st.session_state['navn'] = navn

    st.markdown('<br><br><br>', unsafe_allow_html=True)
    if st.checkbox('Klar ferdig kjør!'):

        st.header('Hællæ %s, nå er vi klare for ALLE MOT SIGRID!!' % st.session_state['navn'])




        for i in range(len(titler)):

            print_oppgave((titler[st.session_state['counter']],
                          tekster[st.session_state['counter']],
                          slider_vals[st.session_state['counter']])
                          )

            if st.checkbox('Se resultat', key='resultat_%s' % st.session_state['counter']):

                fig = plot([3,6,5,3,7,6,5], 4, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
                st.plotly_chart(fig)


                if st.button('Neste oppgave'):
                    st.session_state['counter'] = st.session_state['counter'] + 1
                else:
                    break

            else:
                break




    rows = run_query("SELECT * from oppgavesvar;")

    # Print results.
    with oppgavetittel:
        st.write('\n'.join([f"{row[0]} has a :{row[1]}:" for row in rows]))


    st.write("Add a new name and number to the database")
    name = st.text_input("Name")
    number = st.text_input("Number")

    if st.button("Submit"):
        run_query(f"INSERT INTO oppgavesvar (name, svar) VALUES ('{name}', '{number}');")


if __name__ == '__main__':
    main()
