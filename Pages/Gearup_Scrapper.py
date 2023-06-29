import streamlit as st
import backend2 as backend


st.title("Gearup Scrapper")
value=st.text_input("Enter your Product Id")
if value!="":
    with st.form("My Form"):
        product_link = (backend.create_product_url(value))
        product_info = backend.get_data(product_link)
        file=st.selectbox("Select Category",('Headsets.csv', 'Laptop_Bags.csv', 'Keyboard_Mouse.csv','Monitor.csv','Servers.csv','Printer_Scanners.csv',"Others.csv"))
        brand=st.text_input("Brand", value=f"""{product_info["Brand"]}""")
        model_info=st.text_area("Model_Info", value=f"""{product_info["Model_Info"]}""")
        model_details=st.text_area("Model_Details", value=f"""{product_info["Model_Details"]}""")
        image_link=st.text_input("Image_Link", value=f"""{product_info["Image_Link"]}""")
        st.image(product_info["Image_Link"])
        submitted=st.form_submit_button("submit")
    if (submitted):
        product_info = {}
        product_info["Brand"] = brand
        product_info["Model_Info"] = model_info
        product_info["Model_Details"] = model_details
        product_info["Image_Link"] = image_link
        backend.add_data(product_info,file)

