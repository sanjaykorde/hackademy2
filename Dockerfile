# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
RUN pip install pandas
RUN pip install matplotlib
RUN pip install dash
RUN pip install xlrd

RUN pip install dash_core_components
RUN pip install dash_bootstrap_components
RUN pip install dash_html_components
RUN pip install plotly
RUN pip install matplotlib
RUN pip install sqlite3

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD [ "python", "app.py" ]
