# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use a lightweight base image with Python
FROM python:3.12-slim

# Install uv
RUN pip install --no-cache-dir uv==0.7.13

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container. This includes pyproject.toml and uv.lock
COPY . .

# Use uv sync to install dependencies from uv.lock or pyproject.toml
RUN uv sync --frozen

# Expose the port Streamlit runs on
EXPOSE 8080

# Command to run the Streamlit app, specifying the path to the app file
CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
