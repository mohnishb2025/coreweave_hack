FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# The upstream image can retain an obsolete Yarn APT source whose expired key
# prevents subsequent devcontainer features from installing their packages.
RUN rm -f /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/yarn.sources
