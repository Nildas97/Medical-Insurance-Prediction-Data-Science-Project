# dockerfile
# FROM - installs the program version which is mentioned
FROM python:3.8-slim
# COPY - copies all the data in the file into client's current directory
COPY . /app
# WORKDIR - checks python files and transfers all the data to work directory
WORKDIR /app
# RUN
RUN pip install -r requirements.txt
# EXPOSE 
EXPOSE 80
# CMD
CMD streamlit run streamlit_app.python
