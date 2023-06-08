import streamlit as st
import pandas as pd
from faker import Faker
import base64
import time

timestr = time.strftime("%Y%m&d-%H%M%S")


def gen(number, locale, random_seed=200):
    locale_fake = Faker(locale)
    data = [locale_fake.simple_profile() for i in range(number)]
    df = pd.DataFrame(data)
    return df


def make(data, format="csv"):
    if format == "csv":
        datafile = data.to_csv(index=False)
    elif format == "json":
        datafile = data.to_json()
    b64 = base64.b64encode(datafile.encode()).decode()
    st.markdown("### Download File ###")
    filename = "fake_dataset_{}.{}".format(timestr, format)
    href = f'<a href="data:/file/{format};base64,{b64}" download="{filename}">Click here to download</a>'
    st.write(href, unsafe_allow_html=True)


def main():
    st.title("data generator")
    menu = ["home", "customize", "about"]
    choice = st.sidebar.selectbox("Navigate", menu)
    if choice == "home":
        st.subheader("Generator")
        numgen = st.sidebar.number_input("Number", 10, 5000)
        locale = ["en_US","es"]
        mylocale = st.sidebar.multiselect("Locale", locale, default="en_US")
        dataformat = st.sidebar.selectbox("Save as", ["csv", "json"])
        df = gen(numgen, mylocale)
        st.dataframe(df)
        make(df, dataformat)
    elif choice == "customize":
        st.subheader("Select Custom fields")
        numgen = st.sidebar.number_input("Number", 10, 5000)
        locale = ["en_US","es"]
        mylocale = st.sidebar.multiselect("Locale", locale, default="en_US")
        dataformat = st.sidebar.selectbox("Save as", ["csv", "json"])

        profile_options = [
            "username",
            "email",
            "name",
            "job",
            "company",
            "residence",
            "current_location",
            "website",
            "sex",
            "address",
            "mail",
            "birthdate",
            "snn",
        ]
        profile_fields = st.sidebar.multiselect(
            "fields", profile_options, default="username"
        )
        custom_fake = Faker(locale)
        data = [custom_fake.profile(fields=profile_fields) for i in range(numgen)]
        df = pd.DataFrame(data)
        st.dataframe(df)
        with st.expander("View as json"):
            for i in range(numgen):
                st.write(custom_fake.profile(fields=profile_fields))
        with st.expander("Download file"):
            make(df, dataformat)
    else:
        st.subheader("about")


if __name__ == "__main__":
    main()
